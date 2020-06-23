# Semantic Dual Task
Code for semantic dual task for Perception Lab @ Carleton.

To run this program:
- Open `main.py` in PsycoPy. Make sure to set `is_debug_mode=True` if you only want to test the program quickly; set it to `False` otherwise.

To understand how and why this program words:
- Simply read `main.py` - I've annotated it very extensively so don't fear.

Files and their purposes:
- `sdt_word_lists.csv`: The four word lists in here are imported by `main.py`.
- `tape.json`: This dictionary maps participant id to the order of word lists and noises received by the corresponding participant. I generated this mapping randomly; in reality, this should be generated using counter-balancing.
- `integer_2_noise_order`: This dictionary maps integer index to order of four noises.
- `letter_2_word_list_order`: This dictionary maps integer index to order of four word lists.
- `instructions`: This dictionary maps event to messages that we would like to display to our participants.
- `main.py`: Run this script using PsycoPy. 
- `data`: Data will be saved here. First column: word index; second column: noun response; third column: response time. This need to be analyzed later by referencing `tape.json`. See `./data/12.csv` for an example output file for a hypothetical participant whose id is 12.

TODOs:
- Add noise files
- Finish up instructions
