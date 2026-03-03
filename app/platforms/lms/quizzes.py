"""Quiz grading logic."""

def grade(correct:list[str],answers:list[str])->dict:
    total=max(1,len(correct))
    score=sum(1 for c,a in zip(correct,answers) if c==a)
    percent=round(100.0*score/total,2)
    return {'score':score,'total':total,'percent':percent}
