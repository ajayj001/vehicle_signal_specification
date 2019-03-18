#!/usr/bin/python

#
#
#
# All files and artifacts in this repository are licensed under the
# provisions of the license provided by the LICENSE file in this repository.
#

#
# Convert vspec file to CSV
#

import sys
import vspec
import json
import getopt
import csv

def usage():
    print("Usage:", sys.argv[0], "[-I include_dir] ... [-i prefix:id_file:start_id] vspec_file csv_file")
    print("  -I include_dir              Add include directory to search for included vspec")
    print("                              files. Can be used multiple timees.")
    print()
    print("  -i prefix:id_file:start_id  Add include directory to search for included vspec")
    print("                              files. Can be used multiple timees.")
    print()
    print(" vspec_file                   The vehicle specification file to parse.")
    print(" csv_file                    The file to output the CSV data to.")
    sys.exit(255)

def format_data(json_data):
    Id = '""'
    Type = '""'
    Unit = '""'
    DataType = '""'
    Min = '""'
    Max = '""'
    Desc = '""'
    Enum = '""'
    Sensor = '""'
    Actuator = '""'

    if ('id' in json_data):
        Id = '"' + str(json_data['id']) + '"'
    if ('type' in json_data):
        Type = '"' + json_data['type'] + '"'
    if ('datatype' in json_data):
        DataType = '"' + json_data['datatype'] + '"'
    if ('unit' in json_data):
        Unit = '"' + json_data['unit'] + '"'
    if ('min' in json_data):
        Min = '"' + str(json_data['min']) + '"'
    if ('max' in json_data):
        Max = '"' + str(json_data['max']) + '"'
    if ('description' in json_data):
        Desc = '"' + json_data['description'] + '"'
    if ('enum' in json_data):
        Enum = '"' + ' / '.join(json_data['enum']) + '"'
    if ('sensor' in json_data):
        Sensor = '"' + str(json_data['sensor']) + '"'
    if ('actuator' in json_data):
        Actuator = '"' + str(json_data['actuator']) + '"'
    return Id + ","+ Type + ","+ DataType + ","+ Unit + ","+ Min + ","+ Max + ","+ Desc + ","+ Enum + ","+ Sensor + ","+ Actuator

def json2csv(json_data, file_out, parent_signal):
    for k in list(json_data.keys()):
        if (len(parent_signal) > 0):
            signal = parent_signal + "." + k
        else:
            signal = k

        if (json_data[k]['type'] == 'branch'):
            file_out.write(signal + ',' + format_data(json_data[k]) + '\n')
            json2csv(json_data[k]['children'], file_out, signal)
        else:
            file_out.write(signal + ',' + format_data(json_data[k]) + '\n')

if __name__ == "__main__":
    #
    # Check that we have the correct arguments
    #
    opts, args= getopt.getopt(sys.argv[1:], "I:i:")

    # Always search current directory for include_file
    include_dirs = ["."]
    for o, a in opts:
        if o == "-I":
            include_dirs.append(a)
        elif o == "-i":
            id_spec = a.split(":")
            if len(id_spec) != 3:
                print("ERROR: -i needs a 'prefix:id_file:start_id' argument.")
                usage()

            [prefix, file_name, start_id] = id_spec
            vspec.db_mgr.create_signal_db(prefix, file_name, int(start_id))
        else:
            usage()

    if len(args) != 2:
        usage()

    csv_out = open (args[1], "w")

    try:
        tree = vspec.load(args[0], include_dirs)
    except vspec.VSpecError as e:
        print("Error: {}".format(e))
        exit(255)

    json2csv(tree, csv_out, "")
    csv_out.write("\n")
    csv_out.close()
