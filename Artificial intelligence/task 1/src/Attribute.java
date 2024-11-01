import java.util.HashSet;

class Attribute implements Comparable<Attribute> {
    private String name;
    HashSet<String> possibleValues = new HashSet<>();
    HashSet<Rule> targetRules;
    String question = null;

    Attribute(String name) {
        this.name = name;
        targetRules = new HashSet<>();
    }

    boolean add(String value) {
        return possibleValues.add(value);
    }

    @Override
    public String toString() {
        return name;
    }

    @Override
    public int compareTo(Attribute o) {
        return toString().compareTo(o.toString());
    }
}
