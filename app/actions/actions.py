# # This files contains your custom actions which can be used to run
# # custom Python code.
# #
# # See this guide on how to implement these action:
# # https://rasa.com/docs/rasa/custom-actions

# from typing import Any, Text, Dict, List

# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.events import SlotSet

# from model import *

# with open('data/data_dict.json', encoding='utf8') as json_file:
#     data_dict = json.load(json_file)

# ## TFIDF
# # tfidf_model = TFIDFModel()
# # X = []
# # for data in data_dict.values():
# #     X.append(Preprocessor.text_preprocess(data['question']))
# # tfidf_base_features = tfidf_model.fit_transform(X).toarray()
# # with open('pkl/tfidf_base_features.pkl', 'wb') as f:
# #     pickle.dump(tfidf_base_features, f)
# # with open('pkl/tfidf_model2.pkl', 'wb') as f:
# #     pickle.dump(tfidf_model, f)

# # ## BM25
# # tokens_list = []
# # for data in data_dict.values():
# #     tokens_list.append(Preprocessor.text_preprocess(data['question']).split(' '))
# # bm25_model = BM25Model(tokens_list)
# # with open('pkl/bm25_model2.pkl', 'wb') as f:
# #     pickle.dump(bm25_model, f)
# # ================================================================================
# w2v_model = VNword2vecModel()
# w2v_model.load_nlp(("wiki.vi.vec"))
# with open('pkl/w2v_base_features.pkl', 'rb') as f:
#     w2v_base_features = pickle.load(f)

# with open('pkl/tfidf_model2.pkl', 'rb') as f:
#     tfidf_model = pickle.load(f)
#     print('tfidf_model = ', tfidf_model)
# with open('pkl/tfidf_base_features.pkl', 'rb') as f:
#     tfidf_base_features = pickle.load(f)

# with open('pkl/bm25_model2.pkl', 'rb') as f:
#     bm25_model = pickle.load(f)
#     print('bm25_model = ', bm25_model)

# class ActionAsk(Action):
#     def name(self) -> Text:
#         return "action_ask"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         # print('tracker = ', tracker)
#         # print('tracker events= ', tracker.events)
#         # print('tracker.slots = ', tracker.slots)
#         # print('query = ', query)
#         query = tracker.latest_message['text']
#         if query == '/ask':
#             query = tracker.slots["question"]
#         w2v_res = w2v_model.find_k_most_similar(query, w2v_base_features, 2)
#         # print('w2v_res = ', w2v_res)
#         tfidf_res = tfidf_model.find_k_most_similar(query, tfidf_base_features, 2)
#         bm25_res = bm25_model.find_k_most_similar(query, 2)
#         res_set = set([r[0] for r in w2v_res] + \
#                     [r[0] for r in tfidf_res] + \
#                     [r[0] for r in bm25_res])

#         elements = []

#         for id in list(res_set):
#             a_dict = {}
#             a_dict["title"] = 'Câu hỏi #'+str(id)
#             a_dict["subtitle"] = data_dict[str(id)]['question']
#             # a_dict["image_url"] = "https://lh3.googleusercontent.com/proxy/vfkASNsh6HaWNCvln2MWzUGbscFhHzK-zCg4VCf1wt5V-g3B9bR7XGhdya9BsT72bDWHbaPQZm5Oz-OeX_TbmrdSU3ZebQ1WMlwZa70v-Ej0DIVlu8ysllIodpacLSWoQ0jXWNtqV8QKmMWHfW6RQ-awMg"
#             a_dict["buttons"] = [
#                 {
#                     "type": "postback",
#                     "payload": "/ask_detail{" + str(id) + "}",
#                     "title": "Xem câu trả lời"
#                 }
#             ]
#             elements.append(a_dict)
#         attachment = {}
#         attachment["type"] = "template"
#         attachment["payload"] = {"template_type":"generic", "elements":elements}

#         dispatcher.utter_message(text='Các câu hỏi tương tự:')
#         dispatcher.utter_message(json_message = {"attachment":attachment})

#         return [SlotSet("question", query)]

# class ActionAskDetail(Action):

#     def name(self) -> Text:
#         return "action_ask_detail"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         event_text = ''
#         for event in (list(reversed(tracker.events)))[:3]: # latest 5 messages
#             if event.get("event") == "user":
#                 event_text = event.get("text")
#         data = data_dict[event_text.split('{')[-1].split('}')[0]]
#         ans = 'Đây là câu hỏi thuộc {}.\n{}'.format(data["domain"], data["answer"])
#         dispatcher.utter_message(text=ans)
#         dispatcher.utter_message(text='Anh/Chị có hài lòng với câu trả lời này không?')
#         return []
