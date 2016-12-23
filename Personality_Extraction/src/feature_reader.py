import sys, os, getopt
import pickle
import collections


def load_data(inputfile):
    with open(inputfile, "rb") as f:
        while 1:
            try:
                data = pickle.load(f)
            except EOFError:
                print 'reached end of file'
                break
            print(data['pos_unigram'])



def main(argv):
   inputfile = './pos_data/007solotraveler.pos'
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'feature_reader.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'feature_reader.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print 'Input file is "', inputfile
   load_data(inputfile)
if __name__ == "__main__":
   main(sys.argv[1:])
