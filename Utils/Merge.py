def merge_chunks(chunks_data, output_file):
    with open(output_file, "wb") as opt:
        for chunk in chunks_data:
            opt.write(chunk)