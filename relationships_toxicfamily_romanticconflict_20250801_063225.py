class RelationshipIssue:
    def __init__(self, name):
        self.name = name

class RelationshipProblem:
    def __init__(self, relationships=[]):
        self.relationships = [RelationshipIssue(relation) for relation in relationships]

    def describe_issues(self):
        for relationship in self.relationships:
            print(f"Issue: {relationship.name}")

def main():
    try:
        relationships = ["toxic_family", "romantic_conflict", "friendship_loss"]
        problem = RelationshipProblem(relationships)
        problem.describe_issues()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()