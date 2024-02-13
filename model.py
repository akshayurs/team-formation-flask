from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

def group_users(recommended_candidates,number_of_groups):
  
  """Groups recommended users based on their skills and soft skills using content-based filtering.

  Args:
    recommended_candidates: A list of dictionaries, where each dictionary represents a candidate profile.

  Returns:
    A dictionary where keys are group names and values are lists of candidate names belonging to that group.
  """

  # Extract skills and soft skills from candidate profiles
  candidate_profiles = []
  for candidate in recommended_candidates:
    skills = " ".join(candidate["skills"])
    soft_skills = " ".join([f"{k}:{v}" for k, v in candidate["soft_skills"].items()])
    candidate_profiles.append(f"{skills} {soft_skills}")

  # Create TF-IDF vectorizer
  vectorizer = TfidfVectorizer()
  candidate_vectors = vectorizer.fit_transform(candidate_profiles)

  # Perform K-means clustering
  from sklearn.cluster import KMeans
  number_of_groups=int(number_of_groups)
  kmeans = KMeans(n_clusters=number_of_groups)
  kmeans.fit(candidate_vectors)

  # Assign candidates to groups
  groups = {}
  for i, candidate in enumerate(recommended_candidates):
    group_name = f"Group {kmeans.labels_[i] + 1}"
    if group_name not in groups:
      groups[group_name] = []
    groups[group_name].append(candidate["name"])

  return groups

if __name__ == "__main__":
# Group recommended candidates
    recommended_candidates = [
    {"name": "User1", "skills": ["Python", "JavaScript", "Data Analysis"], "soft_skills": {"Communication": 4, "Teamwork": 5}},
    {"name": "User2", "skills": ["Java", "C++", "Machine Learning"], "soft_skills": {"Leadership": 3, "Problem Solving": 5}},
    {"name": "User3", "skills": ["Python", "R", "Statistics"], "soft_skills": {"Communication": 5, "Time Management": 4}},
    {"name": "User4", "skills": ["Python", "JavaScript", "Data Analysis"], "soft_skills": {"Communication": 4, "Teamwork": 5}},
    {"name": "User5", "skills": ["C", "Docker", "Data Analysis"],  "soft_skills": {"Communication": 5, "Time Management": 4}},
    ]

    number_of_groups=input("Please enter Number of Teams you want to make");
    groups = group_users(recommended_candidates,number_of_groups)

    # Print group information
    for group_name, members in groups.items():
        print(f"{group_name}:", ", ".join(members))

#pickle.dump(groups,open("model.pkl", "wb"))