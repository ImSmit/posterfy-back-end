

def get_or_none(classmodel, pk):
    try:
        data = classmodel.objects.get(_id=pk)
    except classmodel.DoesNotExist as e:
        print("Error: ", e)
        return None
    return data