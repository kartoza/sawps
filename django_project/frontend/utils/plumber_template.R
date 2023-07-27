# plumber.R

library(tidyverse)
library(tidygam)
library(mgcv)
library(ggpubr)

#* Echo back the input
#* @get /echo
function() {
  list(msg = paste0("Plumber is working!"))
}

#* Generic Model
#* @param filepath Path of data file
#* @post /generic
function(filepath) {
  all_data <- read.csv(filepath)
  # do any data cleaning
  cleaned_data <- all_data

  #Now create a list of reserves
  reserves <- split(cleaned_data, cleaned_data$property)

  #Limit only to years with data
  reserves <- lapply(reserves, function(x){
    x[which(!is.na(x$count_total)),]
  })

  #By province
  pr <- unlist(lapply(reserves, function(x) x$province[1]))
  provinces <- unique(cleaned_data$province)

  num.prop.prov <- as.numeric(table(pr))
  p=1
  tot.pop.prov <- lst()
  for (p in 1:length(provinces)) {
    a <- reserves[which(pr == provinces[p])]
    b <- lapply(a, function(x) {
      x$count_total[nrow(x)]
    })
    tot.pop.prov[[p]] <- sum(unlist(b))
  }
  names(tot.pop.prov) <- provinces

  df <- do.call("rbind", tot.pop.prov)
  df <- as_tibble(df)
  df$province <- provinces
  names(df)[1] <- "count_total"
  num.prop.prov <- as.data.frame(table(pr))
  names(num.prop.prov)[1] <- "province"
  names(num.prop.prov)[2] <- "freq"

  population_per_province <- left_join(df, num.prop.prov)

  #Create list with reserve that has 3 or more years of data
  a <- unlist(lapply(reserves, nrow))
  b <- a[which(a>2)]
  reserves_with_3_or_more_years <- reserves[names(b)]

  #######Per Property pop trend----------------------------------------------------
  #Now loop through several reserves
  gam_predictions_per_reserve <- lst()
  population_per_reserve <- lst()
  r=1
  for(r in 1:length(reserves_with_3_or_more_years)){
    res <- reserves_with_3_or_more_years[[r]]
    gam_model <- gam(count_total ~ s(year, k = 3), data = res)
    
    new_data <- data.frame(year = seq(min(res$year), max(res$year), by = 0.5))
    predictions <- predict(gam_model, newdata = new_data, se.fit = TRUE)
    df_predictions <- data.frame(new_data, predictions)
    df_predictions$lower_ci <- with(df_predictions, fit - 3 * se.fit)
    df_predictions$upper_ci <- with(df_predictions, fit + 3 * se.fit)
    gam_predictions_per_reserve[[r]] <- df_predictions
    population_per_reserve[[r]] <- data.frame(res$year, res$count_total)
    colnames(population_per_reserve[[r]]) <- c('year', 'count_total')
  }
  names(gam_predictions_per_reserve) <- names(reserves_with_3_or_more_years)
  names(population_per_reserve) <- names(reserves_with_3_or_more_years)

  #Now the national and provincial
  glst <- lst()
  for (i in 1:length(gam_predictions_per_reserve)){
    glst[[i]] <- data.frame(reserve = names(gam_predictions_per_reserve)[i],
                            gam_predictions_per_reserve[[i]])
  }
  #combine into one data frame
  h <- do.call("rbind", glst)
  #add province
  prop <- cleaned_data %>% select(property, province)
  names(prop)[1] <- "reserve"
  h2 <- left_join(h, prop)

  #######National pop trend----------------------------------------------------
  national_trend <- h2 %>% group_by(year) %>% 
    summarise(fit = sum(fit), se.fit = sum(se.fit))
  national_trend$lower_ci <- with(national_trend, fit - 3 * se.fit)
  national_trend$upper_ci <- with(national_trend, fit + 3 * se.fit)

  ####By province and Year-----------------------------------
  provinces_trend_by_year <- h2 %>% group_by(year,province) %>% 
    summarise(fit = sum(fit), se.fit = sum(se.fit))
  provinces_trend_by_year$lower_ci <- with(provinces_trend_by_year, fit - 2 * se.fit)
  provinces_trend_by_year$upper_ci <- with(provinces_trend_by_year, fit + 2 * se.fit)
  #Group provinces_trend data by its Province name, e.g. 'Gauteng' : {...}
  province_trend_dict <- lst()
  r = 1
  for (r in 1:length(provinces)) {
    province_trend_dict[[r]] <- provinces_trend_by_year %>% filter(province == provinces[r])
  }
  names(province_trend_dict) <- provinces
  
  list(population_per_province = population_per_province, national_trend = national_trend,
       province_trend = province_trend_dict, property_trend = gam_predictions_per_reserve,
       population_per_property = population_per_reserve)
}
