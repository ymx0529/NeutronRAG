from utils.get_question_list import *
from utils.file_operation import save_response


def sort_by_id(input_list):
    """
    Sort a list of dictionaries by the 'id' key in ascending order.

    Args:
        input_list (list): A list of dictionaries, each containing an 'id' key.

    Returns:
        list: A new list sorted by the 'id' key in ascending order.
    """
    # Ensure 'id' key exists in every dictionary
    if not all('id' in d for d in input_list):
        raise ValueError(
            "All dictionaries in the input list must contain the 'id' key.")

    # Sort the list by the 'id' key
    return sorted(input_list, key=lambda x: x['id'])


# path1 = "/home/chency/NeutronRAG/neutronrag/results/analysis/rgb/graphrag/logs/identify_triplets-2025-01-05_13-50-32.json"
# path2 = "/home/chency/NeutronRAG/neutronrag/results/analysis/rgb/graphrag/logs/merged_triplets-2025-01-05_13-51-02.json"

# identify_list = get_question_list(path1)
# sorted_identify_list = sort_by_id(identify_list)

# merged_list = get_question_list(path2)
# sorted_merged_list = sort_by_id(merged_list)


# path1_save = "/home/chency/NeutronRAG/neutronrag/results/analysis/rgb/graphrag/logs/sorted_identify_triplets-2025-01-05_13-50-32.json"
# save_response(sorted_identify_list, path1_save)

# path2_save = "/home/chency/NeutronRAG/neutronrag/results/analysis/rgb/graphrag/logs/sorted_merged_triplets-2025-01-05_13-51-02.json"
# save_response(sorted_merged_list, path2_save)


rgb_path = "/home/chency/NeutronRAG/neutronrag/results/analysis/rgb/graphrag/logs/merged_triplets-2025-01-05_14-22-05.json"
rgbintegration_path = "/home/chency/NeutronRAG/neutronrag/results/analysis/integrationrgb/graphrag/logs/merged_triplets-2025-01-05_22-06-02.json"
identify_list = get_question_list(rgbintegration_path)

all_count = 0
recall_count = 0
for question in identify_list:
    merged_triplets = question["merged_triplets"]
    all_count += len(merged_triplets)
    for each_merge in merged_triplets:
        for each in each_merge:
            if isinstance(each, str):
                recall_count += 1
                break
print(f"all_count:{all_count}")
print(f"recall_count:{recall_count}")
