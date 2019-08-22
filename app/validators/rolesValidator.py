from app import FormValidator


class RolesValidator(FormValidator):

    def __init__(self, formData):
        super().__init__(formData)
        self.addFields()
        self.addConstraints()

    # --------------------------------------------------------------------------------------------------#

    def addFields(self):
        super().addField("name", "Name", "text", required=True)
    # --------------------------------------------------------------------------------------------------#

    def addConstraints(self):
        super().addLengthConstraint("name", 2, 255)