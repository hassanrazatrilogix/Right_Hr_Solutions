from dashboard.models import Service, Cart, Home, Professional_Services, Hr_Solutions, Government, About_Us, FAQSection, get_serializable_data

def populate_original_data(model):
    updated_count = 0
    for instance in model.objects.all():
        if not instance.original_data:
            instance.original_data = get_serializable_data(instance)
            instance.save()
            updated_count += 1
    print(f"Updated {updated_count} records for {model.__name__}.")

populate_original_data(Home)
populate_original_data(Professional_Services)
populate_original_data(Hr_Solutions)
populate_original_data(Government)
populate_original_data(About_Us)
populate_original_data(FAQSection)
