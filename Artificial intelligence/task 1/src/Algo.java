import javax.swing.*;
import java.util.Map;
import java.util.Stack;
import java.util.HashMap;


class Algo {
    private StartAction startAction;
    private KnowledgeBase base = new KnowledgeBase();
    private Stack<TargetValue> targets = new Stack<>();
    private HashMap<Attribute, ContextValue> context = new HashMap<>();
    private boolean isFinished;

    Algo(StartAction startAction, KnowledgeBase base) {
        this.startAction = startAction;
        this.base = base;
    }

    private String nextQuestion(Attribute target) {
        String[] choices = new String[target.possibleValues.size()];
        target.possibleValues.toArray(choices);

        int defaultChoice = 0;

        String input = (String) JOptionPane.showInputDialog(startAction.getMasterComponent(), target.question, target.toString(), JOptionPane.QUESTION_MESSAGE, null, choices, choices[defaultChoice]);

        if (input == null) {
            startAction.writeLine("User canceled data input");
        }

        return input;
    }

    void startAlgo(Attribute target) {
        targets.clear();
        context.clear();
        targets.push(new TargetValue(target, null));
        isFinished = false;
        while (!isFinished) {
            if (targets.empty()) {
                isFinished = true;
                break;
            }
            Attribute current = targets.peek().attribute;
            Rule toAnalize = base.findNextRule(current);
            if (toAnalize != null) {// can find rule
                AnalyzeRule(toAnalize);
            } else {
                if (current.question != null) {
                    String res = nextQuestion(current);
                    if (res == null) {
                        return;
                    }
                    if (!targets.empty()) {
                        toAnalize = targets.pop().rule;
                    }
                    context.put(current, new ContextValue(res, null));
                    startAction.writeLine("Answered: [" + current + " = " + res + "]\n");
                    if (toAnalize != null) {
                        AnalyzeRule(toAnalize);
                    }
                } else {
                    isFinished = true;
                }
            }
        }
        String result = getTargetValue(target);
        if (result != null) {
            startAction.writeLine("Answer: [" + target + " = " + result + "]\n");
        } else {
            startAction.writeLine("Can't find answer!");
        }
    }

    private String getTargetValue(Attribute target) {
        if (!context.containsKey(target)) {
            return null;
        }
        return context.get(target).value;
    }

    private Boolean AnalyzeRule(Rule rule) {
        boolean res = true;
        rule.isAnalyzed = true;
        for (Map.Entry<Attribute, String> entry : rule.conditions.entrySet()) {
            Boolean isRight = checkAttribute(entry.getKey(), entry.getValue());
            if (isRight == null) {
                targets.push(new TargetValue(entry.getKey(), rule));
                startAction.writeLine("Rule #" + rule + " is UNKNOWNN! \t??? [" + entry.getKey() + "]");
                return null;
            } else if (!isRight) {
                startAction.writeLine("Rule #" + rule + " is FALSE!\t[" + entry.getKey() + " != " + entry.getValue() + "]");
                res = false;
                break;
            }
        }
        if (res) {
            context.put(rule.targetAttribute, new ContextValue(rule.targetValue, rule));
            startAction.writeLine("Rule #" + rule + " is TRUE!\t[" + rule.targetAttribute + " = " + rule.targetValue + "]");
            if (targets.empty()) {
                isFinished = true;
            } else {
                targets.pop();
            }
        }
        rule.isCorrect = res;
        return res;
    }

    private Boolean checkAttribute(Attribute att, String val) {
        if (!context.containsKey(att)) {
            return null;
        } else {
            return context.get(att).value.equals(val);
        }
    }

    private class ContextValue {
        String value;
        Rule rule;

        ContextValue(String value, Rule rule) {
            this.value = value;
            this.rule = rule;
        }
    }

    private class TargetValue {
        Attribute attribute;
        Rule rule;

        TargetValue(Attribute attribute, Rule rule) {
            this.attribute = attribute;
            this.rule = rule;
        }
    }

}
