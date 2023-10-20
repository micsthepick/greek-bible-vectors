import argparse
from gensim.models import Word2Vec

def convert_gensim_to_plain_word2vec(input_path, output_path, binary_format=False):
    # Load the gensim Word2Vec model
    model = Word2Vec.load(input_path)

    # Save the model in the original Word2Vec format
    model.wv.save_word2vec_format(output_path, binary=binary_format)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert gensim Word2Vec model to plain Word2Vec format.")

    # Positional arguments for input and output paths
    parser.add_argument("input_path", help="Path to the gensim Word2Vec model.")
    parser.add_argument("output_path", help="Path to save the plain Word2Vec model.")

    # Optional argument to save in binary format
    parser.add_argument("-b", "--binary", action="store_true", help="Save in binary format (default is plain text).")

    args = parser.parse_args()

    convert_gensim_to_plain_word2vec(args.input_path, args.output_path, args.binary)
