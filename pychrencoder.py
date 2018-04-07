import urllib
import optparse
import os

characters_windows1252 = dict()
characters_utf8 = dict()

def fill_chrs_tables(path, delimiter):
    if path == None:
        return
    with open(path, "r+") as echrs:
        for line in echrs.readlines():
            tline = line.replace("\t","").strip()
            chr_array = tline.split(delimiter)
            characters_windows1252[chr_array[0]] = chr_array[1]
            characters_utf8[chr_array[0]] = chr_array[2]


## Simple url encoding, skip ascii characters
def simple_url_encoding(text):
    return urllib.quote_plus(text)


## Full character encoding include ascii characters for e.g: LFI
def full_url_encoding(text, encoded_type):
    if not bool(characters_windows1252) or not bool(characters_utf8):
        print("Use default full url encoding method!\n")
        return urllib.quote_plus(text)
    result = []
    if encoded_type == "win1252":
        for k in text:
            if k in characters_windows1252.keys():
                result.append(characters_windows1252[k])
    elif encoded_type == "utf8":
        for i in text:
            if i in characters_utf8.keys():
               result.append(characters_utf8[i])
    else:
        print("Available types 'win1252' or 'utf8'!")
    return "".join(result)


## Encode the encoded url to bypass filters
def double_url_encoding(text,encoded_type):
    return urllib.quote_plus(full_url_encoding(text, encoded_type))


def encoding_selector(text, elevel, etype):
    if elevel == "0":
        return simple_url_encoding(text)
    elif elevel == "1":
        return full_url_encoding(text, etype)
    elif elevel == "2":
        return double_url_encoding(text, etype)
    return "Available levels 0, 1, 2"

def banner():
    welcome = """
                                                   
 _____ ___ ___ ____  _____ _____ _____ _____ _____ 
| __  |  _| | |    \|  |  |  _  | __  |     |  _  |
| __ -| . |_  |  |  |    -|     |    -| | | |     |
|_____|___| |_|____/|__|__|__|__|__|__|_|_|_|__|__|
                                                   
             URL Encoder Script v1.0
"""
    return welcome


def main():
    os.system('clear')
    print(banner())
    description = "Comments:\n\tDon't specify encoding type if you did not specify file path!\n\tEncoding levels:\n\t\t0 - only encode special characters\n\t\t1 - encode all character not only special characters\n\t\t2 - double encoding (encode the encoded input twice)\n"
    parser = optparse.OptionParser(description+"Usage:\n\t-f Character file, format: A;%41;%41\n\t-i Specify your input \n\t-e URL character encoding type\n\t-l URL encoding level 0-2")
    parser.add_option('-f', dest='fpath', type='string', help='Specify delimited character list (The file contains maximum 3 column e.g: A;%41;%41), optional arguement')
    parser.add_option('-e', dest='etype', type='string', help='Available characer encoding types by default win1252 and utf8')
    parser.add_option('-l', dest='elevel', type='string', help='Specify character URL encoding level 0 to 2')
    parser.add_option('-i', dest='input', type='string', help='Specify your input, you want to encode')
    (options,args) = parser.parse_args()

    msg_out = "URL Encoded result: "

    if (options.fpath == None) & (options.etype == None) & (options.elevel != None) & (options.input != None):
        etype = options.etype
        elevel = options.elevel
        inp = options.input
        output = encoding_selector(inp, elevel, None)
        print(msg_out+output)
    elif (options.fpath != None) & (options.etype != None) & (options.elevel != None) & (options.input != None):
        fpath = options.fpath
        etype = options.etype
        elevel = options.elevel
        inp = options.input
        fill_chrs_tables(fpath,";")
        output = encoding_selector(inp, elevel, etype)
        print(msg_out+output)
    elif (options.fpath == None) | (options.etype == None) | (options.elevel == None) | (options.input == None):
        print(parser.usage)
        exit(0)


if __name__ == "__main__":
    main()
