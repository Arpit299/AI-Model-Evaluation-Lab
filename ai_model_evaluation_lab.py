import argparse
import json
import statistics
import re
from collections import Counter
from pathlib import Path
class EvaluationLab:
    def __init__(self,dataset,outputs):
        self.dataset=dataset
        self.outputs=outputs
    def norm(self,value):
        return re.sub(r"\s+"," ",str(value).strip().lower())
    def tokens(self,text):
        return set(re.findall(r"\b\w+\b",self.norm(text)))
    def accuracy(self,expected,predictions):
        return sum(self.norm(a)==self.norm(b) for a,b in zip(expected,predictions))/len(expected) if expected else 0
    def keyword_score(self,expected,predictions):
        scores=[]
        for expected_value,prediction in zip(expected,predictions):
            e=self.tokens(expected_value)
            p=self.tokens(prediction)
            scores.append(len(e&p)/len(e) if e else 1)
        return statistics.mean(scores) if scores else 0
    def consistency(self,predictions,repeats):
        scores=[]
        for index,prediction in enumerate(predictions):
            variants=repeats[index] if index<len(repeats) else []
            values=[self.norm(prediction)]+[self.norm(x) for x in variants]
            counts=Counter(values)
            scores.append(counts.most_common(1)[0][1]/len(values) if values else 0)
        return statistics.mean(scores) if scores else 0
    def cost(self,predictions):
        total_tokens=sum(20+len(re.findall(r"\b\w+\b",str(x))) for x in predictions)
        return round(total_tokens/1000*0.002,6)
    def evaluate_model(self,name,items):
        expected=[item["expected"] for item in self.dataset]
        predictions=[item.get("prediction","") for item in items]
        if len(predictions)!=len(expected):
            raise ValueError(f"{name}: prediction count must equal dataset size")
        latencies=[float(item.get("latency_ms",0)) for item in items]
        repeats=[item.get("repeats",[]) for item in items]
        accuracy=self.accuracy(expected,predictions)
        keyword=self.keyword_score(expected,predictions)
        consistency=self.consistency(predictions,repeats)
        format_score=sum(isinstance(x,str) and bool(x.strip()) for x in predictions)/len(predictions) if predictions else 0
        average_latency=statistics.mean(latencies) if latencies else 0
        latency_score=1/(1+average_latency/1000) if latencies else 0
        overall=accuracy*.4+keyword*.2+consistency*.15+format_score*.1+latency_score*.15
        return {"model":name,"samples":len(predictions),"accuracy":round(accuracy,4),"keyword_score":round(keyword,4),"consistency":round(consistency,4),"format_score":round(format_score,4),"avg_latency_ms":round(average_latency,3),"latency_score":round(latency_score,4),"estimated_cost_usd":self.cost(predictions),"overall_score":round(overall,4)}
    def evaluate(self):
        models=[self.evaluate_model(name,items) for name,items in self.outputs.items()]
        models.sort(key=lambda item:item["overall_score"],reverse=True)
        leaderboard=[{"rank":index+1,"model":item["model"],"overall_score":item["overall_score"]} for index,item in enumerate(models)]
        return {"dataset_size":len(self.dataset),"models":models,"leaderboard":leaderboard}
def load_jsonl(path):
    rows=[]
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows
def load_outputs(path):
    data=json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data,dict) or not all(isinstance(value,list) for value in data.values()):
        raise ValueError("Outputs JSON must map model names to prediction lists")
    return data
def demo():
    dataset=[{"input":"2+2","expected":"4"},{"input":"Capital of France","expected":"Paris"},{"input":"Sky color","expected":"Blue"},{"input":"What is Python","expected":"Programming Language"},{"input":"3*3","expected":"9"}]
    outputs={"Model-A":[{"prediction":"4","latency_ms":120,"repeats":["4","4"]},{"prediction":"Paris","latency_ms":130,"repeats":["Paris","Paris"]},{"prediction":"Blue","latency_ms":110,"repeats":["Blue","Blue"]},{"prediction":"Programming Language","latency_ms":180,"repeats":["Programming Language","Programming language"]},{"prediction":"9","latency_ms":100,"repeats":["9","9"]}],"Model-B":[{"prediction":"four","latency_ms":80,"repeats":["4","four"]},{"prediction":"Paris","latency_ms":85,"repeats":["Paris","Paris"]},{"prediction":"Blue sky","latency_ms":95,"repeats":["Blue","Blue sky"]},{"prediction":"Programming Language","latency_ms":90,"repeats":["Programming Language","Programming Language"]},{"prediction":"9","latency_ms":75,"repeats":["9","9"]}],"Model-C":[{"prediction":"4","latency_ms":60,"repeats":["4","4"]},{"prediction":"Lyon","latency_ms":65,"repeats":["Paris","Lyon"]},{"prediction":"Green","latency_ms":70,"repeats":["Blue","Green"]},{"prediction":"Software tool","latency_ms":75,"repeats":["Programming Language","Software tool"]},{"prediction":"9","latency_ms":62,"repeats":["9","9"]}]}
    return dataset,outputs
def print_report(report):
    print("AI MODEL EVALUATION LAB")
    print("="*60)
    print(f"Dataset Size: {report['dataset_size']}")
    print("LEADERBOARD")
    for item in report["leaderboard"]:
        print(f"{item['rank']}. {item['model']} | score={item['overall_score']:.4f}")
    print("\nMETRICS")
    for item in report["models"]:
        print(f"{item['model']} | accuracy={item['accuracy']:.4f} | keyword={item['keyword_score']:.4f} | consistency={item['consistency']:.4f} | format={item['format_score']:.4f} | latency={item['avg_latency_ms']:.2f}ms | cost=${item['estimated_cost_usd']:.6f}")
def main():
    parser=argparse.ArgumentParser(prog="ai_model_evaluation_lab")
    parser.add_argument("--dataset",default="")
    parser.add_argument("--outputs",default="")
    parser.add_argument("--json",dest="json_file",default="")
    parser.add_argument("--demo",action="store_true")
    args=parser.parse_args()
    try:
        if args.demo or (not args.dataset and not args.outputs):
            dataset,outputs=demo()
        else:
            if not args.dataset or not args.outputs:
                raise ValueError("Provide --dataset and --outputs together or use --demo")
            dataset=load_jsonl(args.dataset)
            outputs=load_outputs(args.outputs)
        report=EvaluationLab(dataset,outputs).evaluate()
        print_report(report)
        if args.json_file:
            output=Path(args.json_file).expanduser().resolve()
            output.write_text(json.dumps(report,indent=2),encoding="utf-8")
            print(f"Saved: {output}")
    except Exception as error:
        print(f"ERROR: {error}")
        raise SystemExit(1)
if __name__=="__main__":
    main()