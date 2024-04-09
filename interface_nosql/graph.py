
from neo4j import GraphDatabase

class Neo4japp:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def create_nodes(self):
        with self._driver.session() as session:
            session.write_transaction(self._create_person, "Alice")
            session.write_transaction(self._create_person, "Bob")
            session.write_transaction(self._create_person, "Mike")
            session.write_transaction(self._create_bike, "Giant")
            session.write_transaction(self._create_bike, "Trek")

    def delete_all(self):
        with self._driver.session() as session:
            session.write_transaction(self._delete_all_nodes)
            session.write_transaction(self._delete_all_relationships)

    @staticmethod
    def _delete_all_nodes(tx):
        tx.run("MATCH (n) DETACH DELETE n")

    @staticmethod
    def _delete_all_relationships(tx):
        tx.run("MATCH ()-[r]-() DELETE r")

    @staticmethod
    def _create_person(tx, name):
        tx.run("CREATE (:Person {name: $name})", name=name)

    @staticmethod
    def _create_bike(tx, brand):
        tx.run("CREATE (:Bike {brand: $brand})", brand=brand)

    def create_relationship(self):
        with self._driver.session() as session:
            session.write_transaction(self._create_owns_relationship, "Alice", "Giant")
            session.write_transaction(self._create_owns_relationship, "Bob", "Trek")
            session.write_transaction(self._create_maintains_relationship, "Mike", "Giant")

    @staticmethod
    def _create_owns_relationship(tx, person_name, bike_brand):
        tx.run("MATCH (p:Person {name: $person_name}), (b:Bike {brand: $bike_brand}) "
               "CREATE (p)-[:OWNS]->(b)", person_name=person_name, bike_brand=bike_brand)

    @staticmethod
    def _create_maintains_relationship(tx, person_name, bike_brand):
        tx.run("MATCH (p:Person {name: $person_name}), (b:Bike {brand: $bike_brand}) "
               "CREATE (p)-[:MAINTAINS]->(b)", person_name=person_name, bike_brand=bike_brand)

# app usage
if __name__ == "__main__":
    app = Neo4japp("neo4j+s://a5ea6fe5.databases.neo4j.io", "neo4j", "Pok3oqnX5cCDXIpHJbercXu1hukp8cQX3ZASd7_vJe4")

    # Delete all nodes and relationships
    app.delete_all()

    # Create person and bike nodes
    app.create_nodes()

    # Create relationships
    app.create_relationship()

    app.close()
