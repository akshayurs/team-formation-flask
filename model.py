import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import math


LOCATION_WEIGHT = 5
EXPERIENCE_WEIGHT = 10


def balance_groups(imbalanced_array, number_of_members):
    """Balances an imbalanced team by length.

    Args:
        imbalanced_array (list): The imbalanced 2D array.

    Returns:
        list: The balanced 2D array.
    """
    # Calculate the target length for balanced arrays
    print([len(i) for i in imbalanced_array])

    # target_length = int(np.mean([len(arr) for arr in imbalanced_array]))
    target_length = number_of_members

    # Initialize a list to store balanced arrays
    balanced_arrays = []

    # Initialize an array to store extra elements
    extra_elements = []

    # Iterate over the imbalanced arrays
    for i, arr in enumerate(imbalanced_array):
        # Check if the array is longer than the target length
        if len(arr) > target_length:
            # Move elements from the longer array to the balanced array
            balanced_arrays.append(arr[:target_length])
            # Store the extra elements
            extra_elements.extend(arr[target_length:])

        else:
            # Append the array as is
            balanced_arrays.append(arr)

    for i in balanced_arrays:
        while len(i) < target_length and len(extra_elements) != 0:
            i.extend([extra_elements[-1]])
            extra_elements.pop()
    if (len(extra_elements) != 0):
        balanced_arrays.append(extra_elements)
    return balanced_arrays


def group_users(recommended_candidates, number_of_members, parameters):
    """Groups recommended users based on selected parameters using content-based filtering.

    Args:
        recommended_candidates: A list of dictionaries, where each dictionary represents a candidate profile.
        number_of_groups: The number of groups to form.
        parameters: A list of parameters to consider while forming teams.

    Returns:
        A dictionary where keys are group names and values are lists of candidate names belonging to that group.
    """
    # Extract details for selected parameters from recommended_candidates
    number_of_groups = 1
    if (number_of_members < len(recommended_candidates)):
        number_of_groups = math.floor(
            len(recommended_candidates)/number_of_members)
    candidate_profiles = []
    for candidate in recommended_candidates:
        profile = {}
        for param in parameters:
            if param in candidate:
                profile[param] = candidate[param]
        candidate_profiles.append(profile)

    # Convert candidate profiles into text representation
    candidate_texts = []
    for profile in candidate_profiles:
        profile_text = " ".join([f"{k}:{v}" for k, v in profile.items()])
        candidate_texts.append(profile_text)

    # Create TF-IDF vectorizerdfdfdf
    vectorizer = TfidfVectorizer()
    candidate_vectors = vectorizer.fit_transform(candidate_texts)

    # Perform K-means clustering
    number_of_groups = int(number_of_groups)
    kmeans = KMeans(n_clusters=number_of_groups)
    kmeans.fit(candidate_vectors)

    # Assign candidates to groups
    groups = {}
    for i, candidate in enumerate(recommended_candidates):
        group_name = f"Group {kmeans.labels_[i] + 1}"
        if group_name not in groups:
            groups[group_name] = []
        groups[group_name].append(candidate["email"])

    return balance_groups(list(groups.values()), number_of_members)


def recommend_candidates(candidates, role_profile):
    # Extract features from candidate profiles and role profile
    candidate_skills = [profile["skills"] for profile in candidates]
    role_skills = role_profile["skills"]

    # Calculate skill similarity scores
    skill_similarities = np.zeros(len(candidates))
    for i, candidate in enumerate(candidates):
        skill_similarities[i] = 0
        if (role_profile['location']['rigidity'] == "STRICT" and role_profile['location']['name'] != candidates[i]['location']):
            continue

        exp = sum([i['years'] for i in candidate['experience']])
        if (role_profile['experience'] == 'JUNIOR' and exp < 5):
            skill_similarities[i] += EXPERIENCE_WEIGHT
        if (role_profile['experience'] == 'SENIOR' and exp > 5):
            skill_similarities[i] += EXPERIENCE_WEIGHT
        print(candidate['experience'], exp, skill_similarities[i])

    for i, candidate_skills in enumerate(candidate_skills):

        matching_skills = set(candidate_skills.keys()
                              ) & set(role_skills.keys())
        similarity_score = sum(
            role_skills[skill]*candidate_skills[skill] for skill in matching_skills)
        skill_similarities[i] += similarity_score
        if role_profile['location']['rigidity'] == "MODERATE" and role_profile['location']['name'] == candidates[i]['location']:
            skill_similarities[i] += LOCATION_WEIGHT

    # Combine all scores
    total_scores = skill_similarities

    # Sort candidates by score and return recommendations

    res = []
    for candidate, similarity_score in zip(candidates, total_scores):
        candidate['score'] = similarity_score
        res.append(candidate)
    recommended_candidates = sorted(
        res, key=lambda x: x['score'], reverse=True)
    return recommended_candidates
