class BaseDTO:
    def __init__(self, update_dict: dict = None):
        self.update_dict = update_dict  # Ensure update_dict is a dictionary, even if None
        # Delay instantiation to avoid randomization; create only when needed
        self.has_update_data = None
        self.already_updated = False

    def update_original_dto(self):
        if self.already_updated:
            return
        if not self.update_dict:
            raise ValueError("Update section not found in JSON file")

        # store both dictionaries in a list before updating the instance
        original_and_update = []
        original_and_update.append(self.original_dto)
        original_and_update.append(self.update_dict)

        # reinitialize the data object with updated values
        self.has_update_data = self.__class__(self.update_dict)
        # Update current instance values
        for attr, value in vars(self.has_update_data).items():
            if value is not None:
                setattr(self, attr, value)

        # Restore original values for attributes not specified in the Update dictionary
        original, updated = original_and_update
        for key in original.keys():
            if key in original["json_data"] and key not in updated:
                setattr(self, key, original[key])

        self.already_updated = True
