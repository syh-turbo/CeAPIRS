#y_true: 1d-list-like
#y_pred: 2d-list-like
#num: 针对num个结果进行计算（num<=y_pred.shape[1]）
class TopK(object):
    def precision_recall_fscore_k(y_true,y_pred,num=3):
        if not isinstance(y_pred[0],list):
            y_pred=[[each] for each in y_pred]
    #     print(y_pred)
        y_pred=[each[0:num] for each in y_pred]
        unique_label=count_unique_label(y_true,y_pred)
        #计算每个类别的precision、recall、f1-score、support
        res={}
        result=''
        for each in unique_label:
            cur_res=[]
            tp_fn=y_true.count(each)#TP+FN
            #TP+FP
            tp_fp=0
            for i in y_pred:
                if each in i:
                    tp_fp+=1
            #TP
            tp=0
            for i in range(len(y_true)):
                if y_true[i] == each and each in y_pred[i]:
                    tp+=1
            support=tp_fn
            try:
                precision=round(tp/tp_fp,2)
                recall=round(tp/tp_fn,2)
                f1_score=round(2/((1/precision)+(1/recall)),2)
            except ZeroDivisionError:
                precision=0
                recall=0
                f1_score=0
            cur_res.append(precision)
            cur_res.append(recall)
            cur_res.append(f1_score)
            cur_res.append(support)
            res[str(each)]=cur_res
        title='\t'+'precision@'+str(num)+'\t'+'recall@'+str(num)+'\t'+'f1_score@'+str(num)+'\t'+'support'+'\n'
        result+=title
        for k,v in sorted(res.items()):
            cur=str(k)+'\t'+str(v[0])+'\t'+str(v[1])+'\t'+str(v[2])+'\t'+str(v[3])+'\n'
            result+=cur
        sums=len(y_true)
        weight_info=[(v[0]*v[3],v[1]*v[3],v[2]*v[3]) for k,v in sorted(res.items())]
        weight_precision=0
        weight_recall=0
        weight_f1_score=0
        for each in weight_info:
            weight_precision+=each[0]
            weight_recall+=each[1]
            weight_f1_score+=each[2]
        weight_precision/=sums
        weight_recall/=sums
        weight_f1_score/=sums
        last_line='avg_total'+'\t'+str(round(weight_precision,2))+'\t'+str(round(weight_recall,2))+'\t'+str(round(weight_f1_score,2))+'\t'+str(sums)
        result+=last_line
        return result
    #统计所有的类别
    def count_unique_label(y_true,y_pred):
        unique_label=[]
        for each in y_true:
            if each not in unique_label:
                unique_label.append(each)
        for i in y_pred:
            for j in i:
                if j not in unique_label:
                    unique_label.append(j)
        unique_label=list(set(unique_label))
        return unique_label