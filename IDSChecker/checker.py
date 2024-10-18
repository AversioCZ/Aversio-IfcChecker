import sys
import os
import ifcopenshell
import ifctester as tst
from ifctester import ids, reporter
from ifctester.ids import Specification, Ids

cwd = os.path.dirname(os.path.realpath(__file__))

class AversioHtml(tst.reporter.Json):
    def __init__(self, ids: Ids):
        self.entity_limit = 100
        super().__init__(ids)

    def report(self) -> None:
        super().report()
        self.results["version"] = self.ids.info.get("version")
        self.results["copyright"] = self.ids.info.get("copyright")
        self.results["author"] = self.ids.info.get("author")
        self.results["idsdate"] = self.ids.info.get("date")
        self.results["idsdescription"] = self.ids.info.get("description")
        self.results["purpose"] = self.ids.info.get ("purpose")
        self.results["milestone"] = self.ids.info.get("milestone")
        self.results["ifcfilepath"] = ""
        self.results["ifcname"]=""
        self.results["ifcdescription"]=""
        self.results["ifctimestamp"]=""
        for spec in self.results["specifications"]:
            for requirement in spec["requirements"]:
                total_passed_entities = len(requirement["passed_entities"])
                total_failed_entities = len(requirement["failed_entities"])
                requirement["passed_entities"] = self.limit_entities(requirement["passed_entities"])
                requirement["failed_entities"] = self.limit_entities(requirement["failed_entities"])
                requirement["total_failed_entities"] = total_failed_entities
                requirement["total_omitted_failures"] = total_failed_entities - self.entity_limit
                requirement["has_omitted_failures"] = total_failed_entities > self.entity_limit
                requirement["total_passed_entities"] = total_passed_entities
                requirement["total_omitted_passes"] = total_passed_entities - self.entity_limit
                requirement["has_omitted_passes"] = total_passed_entities > self.entity_limit

    def limit_entities(self, entities):
        if len(entities) > self.entity_limit:
            if entities[0]["element_type"]:
                return self.group_by_type(entities)
            return entities[0 : self.entity_limit]
        return entities

    def group_by_type(self, entities):
        results = []
        group_limit = 5
        grouped_by_type = {}
        [grouped_by_type.setdefault(e["element_type"], []).append(e) for e in entities]
        total_entities = 0
        for element_type, entities in grouped_by_type.items():
            for i, entity in enumerate(entities):
                results.append(entity)
                total_entities += 1

                if element_type and i > group_limit:
                    results[-1]["type_name"] = element_type.Name if element_type else "Untyped"
                    if element_type:
                        results[-1]["type_tag"] = element_type.Tag
                        results[-1]["type_global_id"] = element_type.GlobalId
                    results[-1]["extra_of_type"] = len(entities) - i
                    if total_entities == self.entity_limit:
                        return results
                    break

                if total_entities == self.entity_limit:
                    results[-1]["type_name"] = element_type.Name if element_type else "Untyped"
                    if element_type:
                        results[-1]["type_tag"] = element_type.Tag
                        results[-1]["type_global_id"] = element_type.GlobalId
                    results[-1]["extra_of_type"] = len(entities) - i
                    return results
        return results

    def to_string(self) -> str:
        import pystache

        with open(os.path.join(cwd, "templates", "report.html"), "r") as file:
            return pystache.render(file.read(), self.results)

    def sortby_status(self):
        specs = self.results["specifications"]
        sorted_by_values = sorted(specs, key=lambda spec: spec['total_checks'], reverse=True)
        self.results["specifications"] = sorted_by_values
        print(specs)
        print(sorted_by_values)
        

    
    def to_file(self, filepath: str, reptemplatepath: str) -> None:
        import pystache

        with open(reptemplatepath, "r", encoding="utf-8") as file:
            with open(filepath, "w", encoding="utf-8") as outfile:
                return outfile.write(pystache.render(file.read(), self.results))