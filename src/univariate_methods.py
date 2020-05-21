import json
from collections.abc import Iterable
from typing import Tuple
import pandas as pd
import math


def return_fields(file_loc="../data/student_data.csv"):
    '''
    returns the field values from the dataset
    :return:
    '''

    assert isinstance(file_loc, str)

    df = pd.read_csv(file_loc)

    val_details = {'STU_ID':'Student ID', 'X1RACE': 'Student Race', 'X1SEX': 'Student Sex', 'X1SES':'Socioeconomic status',
           'X1SCIEFF':'Student Science Self-efficacy', 'N1COURSE': 'Science Course', 'X1SCIID': 'Scale of student\'s science identity',
           'X1SCIUTI':'Scale of student\'s science utility', 'X1SCIINT': 'Scale of student\'s interest in fall 2009 science course',
           'S1TEFRNDS': 'Time/effort in math/science means not enough time with friends', 'S1TEACTIV':'Time/effort in math/science means not enough time \
            for extracurriculars', 'S1TEPOPULAR':'Time/effort in math/science means 9th grader won\'t be popular', 'S1TEMAKEFUN':'Time/effort in math/science\
             means people will make fun of 9th grader','X1CONTROL':'School Control', 'X1LOCALE': 'School Locale (Urbanicity)',
            'N1SEX': 'Science Teacher’s Sex', 'X1TSRACE': 'Science Teacher’s Race', 'X1TSCERT': 'Science teacher\'s science teaching certification',
           'N1HIDEG':'Science teacher\'s highest degree', 'N1SCIJOB': 'Science teacher held science-related prior to becoming a teacher',
           'N1ALTCERT': 'Science teacher entered profession through alternative certification program', 'N1SCIYRS912': 'Years science teacher has taught high school science',
           'N1GROUP': 'Science teacher has students work in small groups', 'N1INTEREST': 'increasing students\' interest in science',
           'N1CONCEPTS':'teaching basic science concepts', 'N1TERMS': 'important science terms/facts N1SKILLS science process/inquiry skills',
            'S1STCHVALUES': '‘9th grader\'s fall 2009 science teacher values/listens to students\' ideas', 'S1STCHRESPCT': '9th grader\'s fall 2009 science\
            teacher treats students with respect', 'S1STCHFAIR': '9th grader\'s fall 2009 science teacher treats every\
            student fairly', 'S1STCHCONF': '‘9th grader\'s fall 09 science teacher thinks all students can be successful',
           'S1STCHMISTKE': '9th grader\'s fall 09 science teacher think mistakes OK if students learn', 'X3TGPAENG': 'English GPA',
           'X3TGPAMAT' : 'Mathematics GPA', 'X3TGPASCI': 'Science GPA'}

    res = dict()
    for k, v in val_details.items():
        if k in df.columns:
            res[k] = v

    return res


def get_counts(field_name='', file_loc="../data/student_data.csv"):
    '''
    returns frequency counts of the input field from the dataframe
    :param file_loc: path to the csv file
    :param field_name: string, name of the field
    :return: returns a dictionary with frequency distribution
    '''

    assert isinstance(field_name, str)

    df = pd.read_csv(file_loc)

    assert field_name in df.columns
    field_data = df[field_name]

    return field_data.value_counts()


def get_field_data(field_name='', file_loc="../data/student_data.csv"):
    '''
    returns the input field data from the dataframe
    :param field_name: string or list of strings, field name
    :param file_loc: string, path to the dataset
    :return: returns the input field data as pandas series
    '''
    if isinstance(field_name, list) or isinstance(field_name, tuple):
        for e in field_name:
            assert isinstance(e, str)
    else:
        assert isinstance(field_name, str)

    df = pd.read_csv(file_loc)

    field_data = df[field_name]

    return field_data

def get_binned_data(field_name='', width=10, file_loc="../data/student_data.csv"):
    '''
    returns the count of continuous data count seperated by range
    :param field_name: string, field name
    :param file_loc: string, path to the dataset
    :return: returns midnumber of range and the count of data in diffrent range
    '''

    assert isinstance(field_name, str)

    df = pd.read_csv(file_loc)

    assert field_name in df.columns
    field_data = df[field_name]
    Range = max(field_data) - min(field_data)
    bins_num = math.ceil(Range / width)
    bins = list(range(bins_num)) #* int(width)
    for i in range(len(bins)):
        bins[i] *= width

    cut = pd.cut(field_data, bins)
    cut_res = pd.value_counts(cut)  
    res = {}
    res["range"] = list(map(lambda x:x.mid,cut_res.index))
    res["count"] = list(cut_res)
    return res


def get_counts_means_data(fields, color_var='X1SCIEFF', file_loc="../data/student_data.csv") \
        -> Tuple[pd.DataFrame, float]:
    '''
    returns a dataframe with mean and count of groups segregated using input fields
    :param color_var: continuous y variable
    :param fields: list of fields
    :param file_loc: path to the dataframe
    :return: returns a dataframe with info to build a sunburst plot
    '''

    assert isinstance(fields, list), f"fields must be a list, not {type(fields)}"
    assert isinstance(color_var, str), f"color_var must be a string, not {type(fields)}"

    df = pd.read_csv(file_loc)
    df = df[fields + [color_var]]
    color_var_mean = df[color_var].mean()

    assert color_var in df.columns
    assert all([(isinstance(field, str) and field in df.columns) for field in fields])

    df = df.groupby(by=fields)

    flat_df = df.count().reset_index().rename(columns={color_var: 'count'})
    flat_df['mean'] = df.mean()[color_var].values
    return flat_df, color_var_mean


# print(get_counts('X1SEX', file_loc='../data/student_data.csv'))

# print(get_sunburst_data(['X1RACE','X1SEX','N1SEX']))


def get_var_group(group, file="../data/var_group.json"):
    """
    return a list of variables of a certain group
    """
    assert isinstance(file, str)
    assert isinstance(group, str)

    with open(file, "r") as f:
        content = json.load(f)
    
    assert group in content
    
    return content[group]


def get_var_info(file="../data/variables.csv"):
    """
    Usage:
        1. Single variable: get_var_info("N1ALTCERT")
        2. Batch variables: get_var_info(["N1ALTCERT", "N1COURSE"])

    :param name: One or more variables for inquiry
    :return: returns a pd.DataFrame associated with the variable or a
        subset of pd.DataFrame corresponds to each variable in name.
    """
    assert isinstance(file, str)
    
    df = pd.read_csv(file, index_col=0)
    
    # Multiple variables
    return df
