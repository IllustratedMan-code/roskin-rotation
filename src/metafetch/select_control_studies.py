import pandas as pd


class controlStudies:
    def __init__(self, path_to_ireceptor):

        ireceptor_data = pd.read_csv(path_to_ireceptor, sep="\t")
        self.ireceptor_data = ireceptor_data
        number_of_subjects = ireceptor_data.groupby(
            by=["study_id", "study_title", "pcr_target_locus", "pub_ids"]
        ).agg(lambda x: len(set(x)))
        number_of_subjects = number_of_subjects.sort_values(
            by="subject_id", ascending=False
        )
        number_of_subjects = number_of_subjects[["subject_id"]]
        number_of_subjects.reset_index()
        number_of_subjects["subject_id"].sum()
        len(
            ireceptor_data[ireceptor_data["disease_diagnosis_id"] == " "][
                "subject_id"
            ].unique()
        )
        self.number_of_subjects = number_of_subjects

        self.number_of_subjects = self.number_of_subjects.rename(
            columns={"subject_id": "subject_count"}
        )
        # IR_roche = ireceptor_data[ireceptor_data["study_id"] == "IR-Roche-000001"]
        # healthy = IR_roche.groupby("subject_id").agg(lambda x: list(set(x))[0])[
        #     "disease_diagnosis_id"
        # ]
        # healthy_ids = list(healthy[healthy == " "].index)
        # print(IR_roche["repository"].unique())

        # len(IR_roche["subject_id"].unique())

    @property
    def studies_by_number_of_subjects(self):

        return self.number_of_subjects

    def control_repertoires_for_study(self, study_id, selector):
        controls = self.ireceptor_data[self.ireceptor_data["disease_diagnosis"] == " "]
        return controls


if __name__ == "__main__":
    cS = controlStudies("ireceptor-human-IGH-1-13-2025.tsv")
    cS.studies_by_number_of_subjects.to_csv("ireceptor-number-of-subjects.csv")
    print(cS.ireceptor_data["disease_diagnosis_id"].unique())
    print(cS.control_repertoires_for_study("PRJEB1289"))
    # print(cS.studies_by_subjects)
