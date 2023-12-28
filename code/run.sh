# # step 1

python make_panel.py > log.make_panel.py.txt 2>&1

# # step 2

python sort.py > log.sort.py.txt 2>&1

# # step 3

python extraction.py > log.extraction.py.txt 2>&1
