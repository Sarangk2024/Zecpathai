# utils/memory_optimizer.py

def memory_efficient_processing(data_stream):
    for item in data_stream:
        # yield item processed
        yield item * 2
