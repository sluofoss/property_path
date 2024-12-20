# project goal

## one needs to be able to enter information like
- property information like price, location, maintenance fee 
- living in the property for how long.
- portion to rent out
- loan information like projected rent, projected tax liability
- expected year to sell the property.
- initial deposit

## one need to be able generate insight like
- investment return compare to saving account at bank
- expected return compare 


# todo:
- [x] enable download of table with fixed name
- [x] modularize editable table callback set
- [x] enable adding rows to table in the UI
- [x] use editable table as input for price calculation
- [ ] visualize and compare the growth rate of property
- [ ] hide input section
- [ ] allow cross filtering of some sort of graphs?
- [ ] create tabs for different menus
- [ ] create drop down of specific property and check the change of cost by different variables. 
- [ ] host on https://render.com/pricing
    - mentioned here [plotly community](https://community.plotly.com/t/free-hosting-platforms-for-python-web-app/75850/2) as having free tier
- [ ] host on single node ECS cluster 
    - https://docs.github.com/en/actions/use-cases-and-examples/deploying/deploying-to-amazon-elastic-container-service

# project initiation log

```
#https://blog.pecar.me/uv-with-django#using-uv-to-create-a-new-django-project
uv init property_path
uv add django
uv run django-admin startproject property_path .
uv run manage.py runserver
```

