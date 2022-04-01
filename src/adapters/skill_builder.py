import itertools
import requests
import spacy




url = "https://raw.githubusercontent.com/microsoft/SkillsExtractorCognitiveSearch/master/data/skills.json"
response = requests.get(url)
results = response.json()
skills = list(results.keys())

lower_skills = [skill.lower().replace('-', ' ') for skill in skills]

# flat_skills = list(itertools.chain(*lower_skills))

technologies = [
 'AWS', 'Airflow', 'Alteryx', 'Azure', 'Bayes', 'BigQuery', ' C ', 'C#',
  'C++', 'Caffe', 'Calculus', 'Cassandra', 'D3', 'Communication',
   'Databricks', 'Django', 'Data Lake', 'Data Pipeline', 'Deep Learning',
    'Docker', 'Excel', 'ETL', 'EMR', 'Fastai', 'Flask', 'GCP', 'Git',
     'Google Cloud', 'Hadoop', 'Hbase', 'Linear Algenbra'
 'Hive','Java', 'Javascript','Kafka', 'Keras', 'Kubernetes', 'KPI',  'Linux', 
 'Matlab', 'MongoDB','Masters', 'MySQL', 'Linear Algebra', 'Metric', 
 'Natural Language Processing', 'Neural Networks', 'NLP', 'NoSQL','NumPy', 'OOP', 
 'Object Oriented', 'Probability', 'Pandas', 'Perl', 'Phd',  'Pig', 
 'Project Management', 'PyTorch', 'Pyspark', 'Python',
  'Random Forests', ' R ', 'Regression', 
  'Redshift', 'SAS', 'Sklearn', 'SPSS', 
 'SQL', 'Scala', 'Scikit', 'Shell', 'Snowflake', 'Spark', 'Spacy', 
 'Stakeholder', 'Statistics', 'Tableau', 'Testing', 'test driven', 'TDD',
 'TensorFlow', 'postgresql', 'Visualization', 
 'XGboost', 'Catboost', 'Kaggle', 'postgres']

lower_techs = [tech.lower() for tech in technologies]


# regular_list = [[1, 2, 3, 4], [5, 6, 7], [8, 9, 10]]

combined = list(set(lower_techs + lower_skills))
# sp = en_core_web_sm.load()
sp = spacy.load("en_core_web_sm")


stopwords = sp.Defaults.stop_words
remaining_skills = [word for word in combined if not word in stopwords]