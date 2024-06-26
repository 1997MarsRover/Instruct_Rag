class Config:
    # data configs
    folder_path = "src/data/"
    validation_filepath = "src/competition_data/Train.csv"
    submission_filepath = "src/competition_data/SampleSubmission.csv"
    synonyms_filepath = "src/competition_data/ActivityMetricsSynonyms.csv"
    standard_filepath = "src/competition_data/AMKEY_GoldenStandard.csv"

    # processed data configs
    df_valid_path = "src/data/df_valid.csv"
    sub_path = "src/data/sub.csv"


    # unify instruct template
    unifyai_template = """
    You are a data extraction assistant specialized in answering user queries by retrieving key metrics from pieces of retrieved contexts. \n
    Your goal is to ensure accurate mapping of values, and you **MUST** follow company-specific rules. \n

    Query: {question}
    Retrieved Contexts: {context}
    2019 Value: {value_2019}
    2020 Value: {value_2020}
    2021 Value: {value_2021}
    2022 Value: ?

    Pay attention to the following Company-Specific Rules (Enclosed in Backticks):

            ```
        if the query has the name distell and the retrived context sentence has no space between the values just after (Distell Group): /n
                    Remove the leftmost digit and return the remaining value for 2022. 
                    Examples: 
                        Context: "Number of lost days (Distell Group)1161 127 550" 
                        Output: "161" 
                        Context: "Number of work-related fatalities (Distell Group)10 1 0" 
                        Output: "0" 

            if the query has the companies impala rustenburg, impala refineries, marula: 
                    extract the 2022 values for Impala rustenburg, Impala refineries, Marula. 
                    return the aggregate sum of the 2022 values for Impala rustenburg, Impala refineries, Marula. 

            if the query has the company ssw : 
                    extract the 2022 values for SA operations pgm and gold. 
                    Return the aggregate sum of the 2022 values for SA operations pgm and gold. 
            ```

        Task Instructions:
            1. Read and understand the query, context, and company rules. \n
            2. Analyze previous year queries and answers to understand how values were extracted. \n
            3. Repeat step 2 to identify patterns in answer extraction. \n
            4. Generate rules based on understanding from step 3. \n
            5. Follow company-specific rules, extract and confirm the answer's magnitude and units. \n
            6. Is the answer in the same magnitude and units as the previous year's answer? if yes, return the answer else go to step 7. \n
            7. If necessary, align the answer to the same magnitude and units as the previous year's answer. \n
            8. If unable to extract, return 0 to avoid providing inaccurate answers. \n

        Post extraction:
            is the 2022 value following the company specific rules? 
            is the 2022 value in the same magnitude as the previous years values namely: {value_2019} , {value_2020} and {value_2021}?
            If not then do the necessary changes and once all these considerations are fulfilled proceed to give the correct answer

        Output format:
            Answer the user query .\n{format_instructions}
        """

