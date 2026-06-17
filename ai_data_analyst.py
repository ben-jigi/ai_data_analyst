import os
import streamlit as st
from langchain_groq import ChatGroq
import sqlite3
import pandas as pd
from cleaning import basic_cleaning
from cleaning import detect_outliers_iqr,fill_mean,fill_median,fill_mode,drop_constant_columns,remove_outliers_iqr,drop_columns
from database import sql_database 
from database import run_query
from chart import charts
from conversion import dtype_conversion

Window_size=6

if "messages" not in st.session_state:
    st.session_state.messages = []



st.title(" AI Data Analyst")

upload_file=st.file_uploader(" upload the file",
                             type="csv")

if upload_file:
    df=pd.read_csv(upload_file)
    st.dataframe(df.head())
    original_df=df.copy()
    df=basic_cleaning(df)

    mode=st.radio("Choose radio",
                  [ "Data Cleaning",
                   "Data Querying"])
    llm = ChatGroq(
    model="llama-3.3-70b-versatile"
     )
        
    
    if mode == "Data Querying":
        sql_database(df)
        st.success("Data uploaded and stored successfully")

        user_question=st.chat_input("\n Ask anything from the data")

        if user_question:



            st.session_state.messages.append(
            {
                "role":"user",
                "content":user_question
            }


        )

        
            columns=list(df.columns)

            
            recent=st.session_state.messages[-Window_size:]
            history=""
            for message in recent:
                history+= f"""
    {message["role"]}:
    {message["content"]}
    """

            prompt=f"""

You are a SQL Expert:
Provide SQL query for the question

Use Conversation History reference and follow up

Table:
data

Conversation History:
{history}

Question:
{user_question}

Columns:
{columns}

Return only sql query
Dont give any explanations

   """
   
            response=llm.invoke(prompt)
            sql_query=(response.content.replace("```sql","")
                   .replace("```","").strip())
            st.code(sql_query)
            result=run_query(sql_query)
            result_text=result.to_string(index=False)
            prompt=f"""
You are an ai assistant

User Question:
{user_question}

Query Answer:
{result_text}

Follow this format:

Answer: <concise answer>

Chart: <Bar,  Line, or None> 

Rules:

Use None if chart is not useful
Use None if there are no numerical values
Use None if there is only one column
Use Bar  for Category comparisons and only if numerical values are also present
USE Line to analyse trend over time
Answer should be concise
"""
            responses=llm.invoke(prompt)

            response_text=responses.content.split("Chart:")[0].replace("Answer:","").strip()
            chart=responses.content.split("Chart:")[1].strip().upper()
        
            if chart=="NONE":
                st.write(response_text)

            else:
                st.write(response_text)
                charts(chart,result)




            st.session_state.messages.append(
            {"role":"assistant",
             "content":response_text}
             
        )


    elif mode == "Data Cleaning":

        df=dtype_conversion(df)


        def dataset_profile(df):
            profile = ""

            profile += f"""
Rows: {len(df)}

Columns: {len(df.columns)}

Duplicates: {df.duplicated().sum()}

"""

            for col in df.columns:
                profile += f"""
Column: {col}

Datatype: {df[col].dtype}

Missing Values: {df[col].isnull().sum()}

Missing Percentage:
{round(df[col].isnull().mean()*100,2)}

Unique Values:
{df[col].nunique()}

Sample Values:
{df[col].dropna().head(5).tolist()}

"""
            
                if pd.api.types.is_numeric_dtype(df[col]):
                    status = detect_outliers_iqr(df,col)
        

                    profile += f"""
Outlier Status:
{status}

"""         
            
                if df[col].nunique()==len(df):

                    profile +="""

                potential ID column:
                Yes
            """
                else:
                    profile+="""

                potential ID column:
                NO    

            """    

            return profile


        profile = dataset_profile(df)

        

        prompt = f"""
    You are a Senior Data Analyst.

Analyze the dataset profile and recommend
data cleaning actions.

Dataset Profile:

{profile}

Available Cleaning Tools:

fill_mean|column

fill_median|column

fill_mode|column

remove_outliers_iqr|column

drop_constant_columns|column

drop_columns|column

Rules:

1. Use median for skewed numeric columns.
2. Use mean for approximately normal numeric columns.
3. Use mode for categorical columns.
4. Only recommend remove_outliers_iqr if Outlier Status is REMOVABLE.
5. Never recommend outlier removal if Outlier Status is MANUAL_REVIEW.
6. if potential id column is yes then recommend drop_columns
7. if potential id column is No then dont recommend drop_columns
8. Recommend drop_columns if missing percentage is greater than 50.
9. Return only executable actions.

Format:

tool_name|column_name

Example:

fill_mode|Gender

fill_median|LoanAmount

remove_outliers_iqr|LoanAmount



"""
    
        

        response=llm.invoke(prompt)
        actions= response.content.strip().split("\n")
        before_cleaning =""
        before_cleaning += f"""
        Rows:{len(original_df)}

        Columns: {len(original_df.columns)}

        old_Duplicates: {original_df.duplicated().sum()}
        """
        for col in original_df.columns:
            before_cleaning += f"""
            Column_names:{col}

            old_Datatype: {original_df[col].dtype}

            before_Missing_Values: {original_df[col].isnull().sum()}

            before_Missing_Percetage:{round(original_df[col].isnull().mean()*100,2)}

        """
        report=[]
        for action in actions:
           
           if ("|") not in action:
               continue

           tool, column = action.split("|")

           if tool == "fill_mode":
                
                df = fill_mode(df, column)
                report.append(f" filled missing values in {column} using mode")
        
           elif tool == "fill_mean":
               
            

               df = fill_mean(df, column)
               report.append(f" filled missing values in {column} using mean")

           elif tool == "fill_median":
               

               df = fill_median(df, column)
               report.append(f" filled missing values in {column} using median")

           elif tool == "remove_outliers_iqr":
               
 
               df = remove_outliers_iqr(df, column)
               report.append(f" Outliers are removed in {column} ")

           elif tool == "drop_columns":
               
               
               df = drop_columns(df, column)
               report.append(f"  {column} is removed")

        
        st.subheader("Cleaned Dataset")

        st.dataframe(df)


        csv = df.to_csv(index=False)

        st.subheader("Cleaning Report")
        for item in report:
            st.write("✓", item)
        After_cleaning = ""
        After_cleaning += f"""
        new_Rows: {len(df)}

        new_Columns: {len(df.columns)}

        Duplicates: {df.duplicated().sum()}
        """
        for col in df.columns:
            After_cleaning += f"""
            Column_names: {col}

            Datatype: {df[col].dtype}

            Missing_Values: {df[col].isnull().sum()}

            Missing_Percetage:{round(df[col].isnull().mean()*100,2)}
"""
        prompt=f"""

            You are Data cleaning Specialist

            Before cleaning data status:
            {before_cleaning}

            After cleaning data status:
            {After_cleaning}

            Generate:

            1. Cleaning Summary:

            2. EDA Summary:

            3. Strengths:

            4. Weakness:

            5. ML readiness score out of 100

            6. Recommendations
            """

        response=llm.invoke(prompt)

        st.write(response.content)

        st.download_button(
    label="Download Cleaned Dataset",
    data=csv,
    file_name="cleaned_dataset.csv",
    mime="text/csv"
        )

            




        




    
