import java.io.FileInputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Scanner;

class KnowledgeBase {
    private final static String ifString = "Если";
    private final static String thenString = "То";
    private final static String isString = "=";
    private final static String andString = "и";
    private final static String endAttributeToken = ":";
    private HashMap<String, Attribute> attributes = new HashMap<>();
    private HashMap<Integer, Rule> rules = new HashMap<>();
    HashSet<Attribute> targetAttributes = new HashSet<>();

    void initBase(FileInputStream fis) throws IOException {
        Scanner sc = new Scanner(fis);

        while (sc.hasNext() && !sc.hasNextInt()) sc.next();

        while (sc.hasNextInt()) {
            Integer id = sc.nextInt();
            String token;
            Rule rule = new Rule(id);
            if (!sc.hasNext() || !sc.next().equals(ifString)) {
                throw new IOException("cant read rule " + id);
            }
            do {
                Scanner lineScanner = new Scanner(sc.nextLine());
                Attribute attribute = readAttribute(lineScanner);
                String value = readValueToAttribute(lineScanner, attribute);
                rule.addCondition(attribute, value);
                if (!sc.hasNext()) {
                    throw new IOException("cant read rule " + id);
                }
                token = sc.next();
            } while (token.equals(andString));
            if (!token.equals(thenString) || !sc.hasNext()) {
                throw new IOException("cant read rule " + id);
            }
            Scanner lineScanner = new Scanner(sc.nextLine());
            Attribute attribute = readAttribute(lineScanner);
            String value = readValueToAttribute(lineScanner, attribute);
            rule.targetAttribute = attribute;
            rule.targetValue = value;
            attribute.targetRules.add(rule);
            targetAttributes.add(attribute);
            rules.put(id, rule);
        }

        sc.close();
    }

    private Attribute readAttribute(Scanner sc) throws IOException {
        String token = "";
        StringBuilder buffer = new StringBuilder();
        while (sc.hasNext() && !isString.equals(token)) {
            buffer.append(token);
            buffer.append(" ");
            token = sc.next();
        }
        String name = buffer.toString().trim();
        if ("".equals(name)) {
            throw new IOException("cant read Attribute");
        }
        return attributes.computeIfAbsent(name, k -> new Attribute(name));
    }

    private String readValueToAttribute(Scanner sc, Attribute attribute) throws IOException {
        StringBuilder buffer = new StringBuilder();
        while (sc.hasNext()) {
            buffer.append(" ");
            buffer.append(sc.next());
        }
        String value = buffer.toString().trim();
        if ("".equals(value)) {
            throw new IOException("cant read Attribute: " + attributes + " because of wrong value");
        }
        attribute.add(value);
        return value;
    }

    void resetRules() {
        for (Rule r : rules.values()) {
            r.isAnalyzed = false;
            r.isCorrect = null;
        }
    }

    void initQuestions(FileInputStream fis) throws IOException {
        Scanner sc = new Scanner(fis, StandardCharsets.UTF_8.name());
        while (sc.hasNext()) {
            String name = sc.nextLine().replace(endAttributeToken, "").trim();
            if (sc.hasNext()) {
                String question = sc.nextLine().trim();
                Attribute attribute = attributes.get(name);
                if (attribute != null && !"".equals(question)) {
                    attribute.question = question;
                    continue;
                }
            }
            throw new IOException("Can't read question for attribute " + name);
        }
    }

    Rule findNextRule(Attribute target) {
        for (Rule rule : target.targetRules) {
            if (!rule.isAnalyzed) {
                return rule;
            }
        }
        return null;
    }
}
