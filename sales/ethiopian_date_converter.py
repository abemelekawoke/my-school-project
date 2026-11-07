# ethiopian_date_converter.py

class EthiopianDateConverter:
    @staticmethod
    def to_gregorian(year, month, day):
        # Basic conversion formula, adjust as per Ethiopian calendar rules
        # This is a simplified example and may not cover all cases
        # Ethiopian calendar calculations are more complex and may require a library or detailed algorithms
        # Example assumes a fixed offset, but actual conversion may require more nuanced rules
        gregorian_year = year + 8
        gregorian_month = month + 2
        gregorian_day = day + 10

        return gregorian_year, gregorian_month, gregorian_day

    @staticmethod
    def from_gregorian(gregorian_year, gregorian_month, gregorian_day):
        # Reverse conversion from Gregorian to Ethiopian
        # Implement as per your specific requirements
        # This is a basic example and may need adjustments
        ethiopian_year = gregorian_year - 8
        ethiopian_month = gregorian_month - 2
        ethiopian_day = gregorian_day - 10

        return ethiopian_year, ethiopian_month, ethiopian_day

# You can add more methods or adjust the existing ones based on your needs
