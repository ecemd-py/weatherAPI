# Formatting the weather info data that is sent to API in request
class WeatherInfoModel:
    time: None 
    location: None 
    condition: None 
    temperature: None
    agg: None
    agg_column: None
    start_date: None
    end_date: None

    @staticmethod
    def parse(dict):
        weather_model = WeatherInfoModel()
        weather_model.time = dict.get("time")
        weather_model.location = dict.get("location")
        weather_model.condition = dict.get("condition")
        weather_model.temperature = dict.get("temperature")
        weather_model.agg = dict.get("agg")
        weather_model.agg_column = dict.get("agg_column")
        weather_model.start_date = dict.get("start_date")
        weather_model.end_date = dict.get("end_date")

        if not weather_model.agg is None and not weather_model.agg in ["MAX", "MIN", "AVG"]:
            raise Exception("AGG function should be MAX, MIN or AVG")
        
        if not weather_model.agg_column is None and not weather_model.agg_column in ["temperature", "time"]:
            raise Exception("AGG column should be 'temperature' or 'time'")
        
        if not weather_model.agg is None and weather_model.agg_column is None:
            raise Exception("If there is AGG function, agg_column should not be empty!")
        
        if weather_model.agg is None and not weather_model.agg_column is None:
            raise Exception("If there is agg_column, AGG function should not be empty!")
        
        if not weather_model.start_date is None and not weather_model.end_date is None:
            if weather_model.end_date < weather_model.start_date:
                raise Exception("End date is before the given start day!")

        return weather_model