# JiangHao
from py2neo import Graph


class GraphSearcher:
    def __init__(self):
        # 连接neo4j数据库
        self.g = Graph("http://127.0.0.1:7474", auth=("neo4j", "Jh8291398"))
        # 限制显示条数
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''

    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            # 获取问题类型
            question_type = sql_['question_type']
            # 获取sql查询语句
            queries = sql_['sql']
            answers = []
            # 执行所有sql语句
            for query in queries:
                # 将数据插入插入到answers中
                ress = self.g.run(query).data()
                print(ress)
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            # final_answer不为空则插入
            if final_answer:
                final_answers.append(final_answer)

        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''

    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'disease_symptom':
            desc = [i['n.name'] for i in answers[:self.num_limit]]
            subject = answers[0]['m.name']
            final_answer = {
                'entity': subject,
                'relation': '症状',
                'object': desc
            }

        elif question_type == 'symptom_disease':
            desc = [i['m.name'] for i in answers[:self.num_limit]]
            subject = answers[0]['n.name']
            final_answer = {
                'entity': subject,
                'relation': '可能染上的疾病',
                'object': desc
            }

        elif question_type == 'disease_cause':
            desc = [i['m.cause'] for i in answers[:self.num_limit]]
            subject = answers[0]['m.name']
            final_answer = {
                'entity': subject,
                'relation': '原因',
                'object': desc
            }

        elif question_type == 'disease_prevent':
            desc = [i['m.prevent'] for i in answers[:self.num_limit]]
            subject = answers[0]['m.name']
            final_answer = {
                'entity': subject,
                'relation': '预防措施',
                'object': desc
            }

        elif question_type == 'disease_lasttime':
            desc = [i['m.cure_lasttime'] for i in answers[:self.num_limit]]
            subject = answers[0]['m.name']
            final_answer = {
                'entity': subject,
                'relation': '治疗可能持续的周期',
                'object': desc
            }

        elif question_type == 'disease_cureway':
            desc = [i['m.cure_way'] for i in answers[:self.num_limit]]
            subject = answers[0]['m.name']
            final_answer = {
                'entity': subject,
                'relation': '尝试治疗方案',
                'object': desc
            }

        elif question_type == 'disease_cureprob':
            desc = [i['m.cured_prob'] for i in answers[:self.num_limit]]
            subject = answers[0]['m.name']
            final_answer = {
                'entity': subject,
                'relation': '治愈的概率',
                'object': desc
            }

        elif question_type == 'disease_easyget':
            desc = [i['m.easy_get'] for i in answers[:self.num_limit]]
            subject = answers[0]['m.name']
            final_answer = {
                'entity': subject,
                'relation': '易感人群',
                'object': desc
            }

        elif question_type == 'disease_desc':
            desc = [i['m.desc'] for i in answers[:self.num_limit]]
            subject = answers[0]['m.name']
            final_answer = {
                'entity': subject,
                'relation': '描述',
                'object': desc
            }

        elif question_type == 'disease_acompany':
            desc1 = [i['n.name'] for i in answers[:self.num_limit]]
            desc2 = [i['m.name'] for i in answers[:self.num_limit]]
            subject = answers[0]['m.name']
            desc = [i for i in desc1 + desc2 if i != subject]
            final_answer = {
                'entity': subject,
                'relation': '症状',
                'object': desc
            }

        elif question_type == 'disease_not_food':
            desc = [i['n.name'] for i in answers[:self.num_limit]]
            subject = answers[0]['m.name']
            final_answer = {
                'entity': subject,
                'relation': '忌食的食物',
                'object': desc
            }

        elif question_type == 'disease_do_food':
            do_desc = [i['n.name'] for i in answers[:self.num_limit] if i['r.name'] == '宜吃']
            recommand_desc = [i['n.name'] for i in answers[:self.num_limit] if i['r.name'] == '推荐食谱']
            subject = answers[0]['m.name']

            final_answer = {
                'entity': subject,
                'relation': '宜食的食物',
                'object': do_desc
            }

        elif question_type == 'food_not_disease':
            desc = [i['m.name'] for i in answers[:self.num_limit]]
            subject = answers[0]['n.name']

            final_answer = {
                'entity': subject,
                'relation': '不宜食的食物',
                'object': desc
            }

        elif question_type == 'food_do_disease':
            desc = [i['m.name'] for i in answers[:self.num_limit]]
            subject = answers[0]['n.name']

            final_answer = {
                'entity': subject,
                'relation': '建议',
                'object': desc
            }

        elif question_type == 'disease_drug':
            desc = [i['n.name'] for i in answers[:self.num_limit]]
            subject = answers[0]['m.name']

            final_answer = {
                'entity': subject,
                'relation': '通常的使用的药品',
                'object': desc
            }

        elif question_type == 'drug_disease':
            desc = [i['m.name'] for i in answers[:self.num_limit]]
            subject = answers[0]['n.name']

            final_answer = {
                'entity': subject,
                'relation': '主治的疾病',
                'object': desc
            }

        elif question_type == 'disease_check':
            desc = [i['n.name'] for i in answers[:self.num_limit]]
            subject = answers[0]['m.name']

            final_answer = {
                'entity': subject,
                'relation': '检查方式',
                'object': desc
            }

        elif question_type == 'check_disease':
            subject = answers[0]['n.name']

            final_answer = {
                'entity': subject,
                'relation': '能检查出来的疾病',
                'object': desc
            }

        return final_answer


if __name__ == '__main__':
    graphSearcher = GraphSearcher()
    data = graphSearcher.search_main(
        [{'question_type': 'disease_cureway', 'sql': ["MATCH (m:Disease) where m.name = '感冒' return m.name, m.cure_way"]}])
    print(data)
