# Austin Bikeshare data analysis

As a part of Stream Processing and Stream Analytics project.

### Project contributers
- [Mr Philosopher](https://github.com/7ze)
- [Usama Tahir](https://github.com/Usama00004)

> **Project Disclaimer**
>Please note that this project is currently under active development. The
>information provided in this readme and associated documentation is subject to
>change without prior notice. While we strive to provide accurate and
>up-to-date details, certain aspects of the project may be modified, added, or
>removed as development progresses.

### Analysis Summary
---

This project aims to conduct comprehensive data analysis on Austin Bikeshare
trips using real-time streaming data. Through advanced data transformations and
insights generation, this analysis seeks to uncover valuable patterns and
trends that can inform decision-making and operational improvements within the
bikeshare system.

#### Analysis Ideas

1. *Subscriber Type Analysis:*
   - Explore the distribution of subscriber types (e.g., Pay-as-you-ride,
     Local365).
   - Identify trends in usage patterns based on different subscriber
     categories.
   
2. *Popular Stations and Routes:*
   - Determine the most frequently used start and end stations.
   - Uncover common routes taken by bikeshare users for optimization.

3. *Duration Analysis:*
   - Analyze trip durations to understand average length and identify
     exceptional cases.
   - Explore correlations between trip duration and other factors.

4. *Bike Usage Analysis:*
   - Investigate bike usage patterns to identify popular bikes and maintenance
     trends.
   - Examine the relationship between bike type and usage frequency.

5. *Time-based Patterns:*
   - Study usage patterns based on time of day, weekdays vs. weekends, and
     months.
   - Identify peak usage hours and seasonal trends.

6. *Subscriber Behavior:*
   - Analyze how subscriber types influence trip behaviors such as trip
     duration and station choices.
   - Determine if different subscriber types have distinct usage patterns.

7. *Station Popularity Over Time:*
   - Track popularity changes of specific stations over time.
   - Investigate factors influencing shifts in station popularity.

8. *Subscriber Retention Analysis:*
   - Explore whether different subscriber types exhibit varying retention
     rates.
   - Understand which types of users tend to continue using the service over
     time.

9. *Bike Availability:*
   - Investigate bike availability at stations and its impact on user behavior.
   - Analyze how bike availability affects station popularity.

10. *Subscriber Demographics (If Available):*
    - Correlate subscriber types with demographic information if available.
    - Understand if certain types of users are more likely to use the service.

11. *Ride Patterns by Day of the Week:*
    - Observe how usage patterns change across different days of the week.
    - Determine if certain days have higher usage due to specific events or
      reasons.

#### Final Dataset Schema idea

```plaintext 
Table: analysis

Fields:
- trip_id: STRING (Primary Key)
- subscriber_type: STRING
- bike_id: STRING
- bike_type: STRING
- start_time: TIMESTAMP
- start_station_id: INTEGER
- start_station_name: STRING
- end_station_id: INTEGER
- end_station_name: STRING
- duration_minutes: INTEGER
- day_of_week: INTEGER
- hour_of_day: INTEGER
- month: INTEGER
- route: STRING
- is_weekend: BOOLEAN
- is_peak_hour: BOOLEAN
- subscriber_demographics: STRING
- subscriber_retention: BOOLEAN
- bike_availability: INTEGER
- station_popularity: INTEGER
- ...

Indexes:
- trip_id (Primary Key) ```
