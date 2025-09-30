import json
import ray


if __name__ == '__main__':

    # Increase number of CPUs as needed, for example: ray.init(num_cpus=6)
    ray.init()

    # Number reduction function
    def reduce_number(original_number: int) -> str:
        """
        Repeatedly subtracts powers of 10 from the number until
        it is reduced to a two-digit number.
        Tracks how many major reduction steps it took.
        Returns a string in the format: "<steps><final_two_digits>"
        """
        major_steps = 1
        keep_reducing = True

        while keep_reducing:
            # Determine the largest power of 10 to subtract
            num_digits = len(str(original_number)) - 2
            subtractor_str = "1" + "0" * num_digits
            subtractor = int(subtractor_str)
            major_steps += 1

            # Subtract repeatedly while result is still > 10
            for _ in range(10):
                test_value = original_number - subtractor
                if test_value > 10:
                    original_number = test_value

            # Format step count as string (with leading zero if < 10)
            step_str = f"{major_steps:02d}"

            # Stop once the number is reduced to 2 digits
            if len(str(original_number)) == 2:
                keep_reducing = False

        return step_str + str(original_number)

    # Ray worker function
    @ray.remote
    def build_lookup_table(start: int, end: int, chunk_id: str) -> str:
        """
        For numbers between start and end (inclusive),
        apply the reduction function and group numbers
        by their reduced signature.

        Writes the lookup dictionary to a JSON file named by chunk_id.
        Returns the file path.
        """
        lookup_dict = {}

        while start <= end:
            reduced_value = reduce_number(start)

            # Append number to its corresponding reduced key
            if reduced_value not in lookup_dict:
                lookup_dict[reduced_value] = []
            lookup_dict[reduced_value].append(start)

            start += 1

        # Save results to JSON file
        file_path = f"./tables/{chunk_id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(lookup_dict, f, ensure_ascii=False, separators=(',', ':'))

        return file_path

    
    # Range definitions
    
    lower_bound = 1199999   # Start of the range
    upper_bound = 7599999   # End of the range
    chunk_end = 1209999     # Temporary placeholder (reset later)

    chunk_jobs = []   # Will hold job configurations

    
    # Split work into chunks
    
    while True:
        print(lower_bound)

        # Step forward
        lower_bound += 1
        if lower_bound >= upper_bound:
            break

        # Use the first 3 digits of the chunk's start as ID
        chunk_id = str(lower_bound)[:3]

        # Define chunk of 10,000 numbers
        chunk_end = lower_bound + 9999

        # Save (start, end, id) for later dispatch
        chunk_jobs.append([lower_bound, chunk_end, chunk_id])

        # Move to the next chunk
        lower_bound = chunk_end

    print(f"Total chunks created: {len(chunk_jobs)}")

    
    # Dispatch jobs to Ray
    
    ray_futures = [
        build_lookup_table.remote(start, end, chunk_id)
        for (start, end, chunk_id) in chunk_jobs
    ]

    total_jobs = len(ray_futures)

    
    # Track progress as jobs finish
    
    for _ in range(1000):
        ready, not_ready = ray.wait(ray_futures)

        # Collect completed jobs
        ray.get(ready)

        # Update remaining list
        ray_futures = not_ready

        # Print progress
        percent_done = int((1.0 - len(ray_futures) / total_jobs) * 100)
        print(f"{percent_done}% complete: {len(not_ready)} jobs remaining")

        if not ray_futures:
            break
