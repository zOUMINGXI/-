import pandas as pd
import json
def get_relation_course_field():
    data = pd.read_json("course-field.json", lines=True)
    return data