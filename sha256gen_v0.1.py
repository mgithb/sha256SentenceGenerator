import dill
import multiprocessing
import itertools
import hashlib
import time

# Override the default picklers
multiprocessing.connection.REDUCE_CONNECTION = dill.dumps
multiprocessing.connection.BUILD_CONNECTION = dill.loads

def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def find_sentence(args):
    starts, parts = args
    sentence_parts = parts[:-1]
    last_part = parts[-1]
    sentence = "The SHA256 for this sentence begins with: {} and {}.".format(", ".join(sentence_parts), last_part)
    digest = sha256(sentence)
    if digest.startswith(starts):
        return (digest, starts, sentence)

def generate_tasks(indexes, chars, words, length):
    for permutation in itertools.permutations(indexes, length):
        starts = ''.join(chars[i] for i in permutation)
        parts = [words[i] for i in permutation]
        yield (starts, parts)

if __name__ == '__main__':
    indexes = list(range(16))
    chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "a", "b", "c", "d", "e", "f"]
    length = 2

    start = time.time()
    last_update_time = start

    pool = Pool(cpu_count())
    max_length = 5  # or whatever you deem appropriate

    while length <= max_length:
        tasks = generate_tasks(indexes, chars, words, length)
        results = pool.map(find_sentence, tasks)
        
        for result in results:
            if result:
                digest, starts, sentence = result
                elapsed_time = (time.time() - start) * 1000
                print(f"milliseconds: {elapsed_time:.2f}, digest: {digest}, starts: {starts}, sentence: {sentence}")

        current_time = time.time()
        if current_time - last_update_time > 600:
            elapsed_time = (current_time - start) * 1000
            print(f"milliseconds since start: {elapsed_time:.2f}, hashes calculated so far: {len(chars)**length}")
            last_update_time = current_time
        
        length += 1

    pool.close()
    pool.join()
