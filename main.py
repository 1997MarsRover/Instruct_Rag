import argparse
from src.services.retrieval import Retrieval
from src.services.embeddings import Embeddings
from src.services.llms import Llms
from src.helpers.config import Config
from src.helpers.utils import prepare_sub_data, prepare_train_data
from langchain_core.runnables import ConfigurableField 

parser = argparse.ArgumentParser(description='retrieval and generation')
parser.add_argument('--vector_store', type=str, default='chroma', help='vector store')
parser.add_argument('--index_name', type=str, default='index', help='index name')
parser.add_argument('--model_provider', type=str, default='huggingface', help='model provider')
parser.add_argument('--model_name', type=str, default='', help='model name')
parser.add_argument('--embedding_provider', type=str, default='huggingface', help='embedding provider')
parser.add_argument('--year', type=str, default='2022', help='year')

args = parser.parse_args()

if __name__ == "__main__":
    df_valid = prepare_train_data(train_filepath=Config.train_filepath, synonyms_path=Config.synonyms_path, standard_path=Config.standard_path)
    df_sub = prepare_sub_data(sub_filepath=Config.sub_filepath, synonyms_path=Config.synonyms_path, standard_path=Config.standard_path)
    llm = Llms(model_provider=args.model_provider, model_name=args.model_name).get_chat_model()
    fallback_llm_1 = Llms(model_provider='google', model_name="gemini-pro").get_chat_model()

    model = (
        llm
        .with_fallbacks([fallback_llm_1])
        .configurable_alternatives(
            ConfigurableField(id = "model"),
            default_key = "llm",
            llm = llm,
            fallback_llm_1 = fallback_llm_1,
        )
    )

    retrieval = Retrieval(vector_store=args.vector_store, index_name=args.index_name)
    embeddings = Embeddings(embedding_provider=args.embedding_provider)

    while True:
        for row in df_sub.itertuples():
            try:
                if row.ID not in df_valid.ID.unique():
                    # if not in train data, then assign a zero as the prediction
                    df_sub.loc[df_sub['ID'] == row.ID, 'Value'] = 0

                else:
                    print(f"Query: {row.query}")
                    print(f"Prev_query_answer_pair: {df_valid[df_valid['ID'].isin([row.ID])]['example'].unique()}")
                    
                    answer = retrieval.retrieve_and_generate(embedding_function=embeddings.get_embedding_function(), query=row.query, previous_year_queries_answer_pairs=df_valid[df_valid['ID'].isin([row.ID])]['example'].unique(), template=Config.unifyai_template, llm=model)
                    print(f"Answer: {answer}")
                    break
            except Exception as e:
                print(f"Error: {e} in row: {row}")
        