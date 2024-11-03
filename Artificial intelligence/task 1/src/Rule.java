import java.io.IOException;
import java.util.HashMap;

class Rule {
    private Integer id;
    HashMap<Attribute, String> conditions = new HashMap<>();
    Attribute targetAttribute;
    String targetValue;
    boolean isAnalyzed;
    Boolean isCorrect;

    Rule(Integer id) {
        this.id = id;
    }

    void addCondition(Attribute attribute, String value) throws IOException {
        String prevValue = conditions.put(attribute, value);
        if (prevValue != null) {
            throw new IOException("attribute with name " + attribute + " was overrided in rule " + id);
        }
    }

    @Override
    public String toString() {
        return id.toString();
    }
}
