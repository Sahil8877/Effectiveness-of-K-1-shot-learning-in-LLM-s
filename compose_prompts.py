import pandas as pd

class query_document_pair:
    def __init__(self, qid: str, docno: str, qText: str, dText: str, qrel: int, score: float):
        self.qid = qid
        self.docno = docno
        self.qText = qText
        self.dText = dText
        self.qrel = qrel
        self.rsv = score
        self.pred = None

    def put_prediction(self, pred: float):
        self.pred = pred
    
    def __str__(self) -> str:
        return f'qid_{self.qid}: {self.qText}; docno_{self.docno}; qrel: {self.qrel}; bm25_rsv: {self.rsv}.'

def get_msmarco_passage_pairs(dataset: str):
    if('v2' not in dataset):
        dl_p1_res_df = pd.read_csv('./res/bm25_dl_19.csv')
        dl_p2_res_df = pd.read_csv('./res/bm25_dl_20.csv')
        queries = pd.read_csv('./middle_products/queries.csv') #####changed to 19
        qrels = pd.read_csv('./middle_products/qrels.csv')
        qrels['docno'] = qrels.docno.astype('str')
    else:
        dl_p1_res_df = pd.read_csv('./res/bm25_dl_21.csv')
        dl_p2_res_df = pd.read_csv('./res/bm25_dl_22.csv')
        queries = pd.read_csv('./middle_products/queries_v2.csv')
        qrels = pd.read_csv('./middle_products/qrels_v2.csv')
        qrels['docno'] = qrels.docno.astype('str')        

    dl_p1_qids = dl_p1_res_df.qid.unique()
    dl_p2_qids = dl_p2_res_df.qid.unique()

    with open(f'./middle_products/{dataset}.pkl', 'rb') as f:
        import pickle
        msmarco_doc_dict = pickle.load(f)
        f.close()

    q_d_pair_list = []
    for qid in dl_p1_qids:
        qText = queries[queries.qid==qid]['query'].tolist()[0]
        df_for_qid = dl_p1_res_df[dl_p1_res_df.qid == qid].sort_values(['rank'], ascending=True)
        denoted_docnos = qrels[qrels.qid == qid].docno.tolist()
        print(df_for_qid.shape)
        
        for docno, score in df_for_qid[['docno', 'score']].values[:100]:
            if('v2' not in dataset):
                docno=str(int(docno))
            dText = msmarco_doc_dict[docno]
            
            if(docno in denoted_docnos):
                qrel = qrels[(qrels.qid==qid) & (qrels.docno==docno)].label.tolist()[0]
            else:
                qrel = -1
            
            q_d_pair = query_document_pair(qid=str(qid), docno=str(docno), qText=qText, dText=dText, qrel=qrel, score=float(score))
            q_d_pair_list.append(q_d_pair)
            # print(q_d_pair)
        
        del(df_for_qid)
        
    for qid in dl_p2_qids:
        
        qText = queries[queries.qid==qid]['query'].tolist()[0]
        df_for_qid = dl_p2_res_df[dl_p2_res_df.qid == qid].sort_values(['rank'], ascending=True)
        denoted_docnos = qrels[qrels.qid == qid].docno.tolist()
        
        for docno, score in df_for_qid[['docno', 'score']].values[:50]:
            if('v2' not in dataset):
                docno=str(int(docno))
            dText = msmarco_doc_dict[docno]
            
            if(docno in denoted_docnos):
                qrel = qrels[(qrels.qid==qid) & (qrels.docno==docno)].label.tolist()[0]
            else:
                qrel = -1
            
            q_d_pair = query_document_pair(qid=str(qid), docno=str(docno), qText=qText, dText=dText, qrel=qrel, score=float(score))
            q_d_pair_list.append(q_d_pair)
            # print(q_d_pair)
        
        del(df_for_qid)

    return q_d_pair_list

# def get_msmarco_passage_pairs():
#     get_msmarco_passage_pairs('msmarco_passage')

# print(q_d_pair_list)