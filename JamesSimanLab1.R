library(tidyverse)

data = read.csv("WoolworthsDemand2024.csv", check.names = FALSE)
tidy_data = data |>
  pivot_longer(
    cols = starts_with("2024"),
    names_to = "Date",
    values_to = "Demand",
    values_drop_na = TRUE
  )

