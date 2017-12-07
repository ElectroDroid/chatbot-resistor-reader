import sys


# Load the data that PHP sent us
try:
    data = sys.argv[1]
except:
    print "ERROR"
    sys.exit(1)

# Generate some data to send to PHP
result = 'Python Connected!'

# Send it to stdout (to PHP)
print result