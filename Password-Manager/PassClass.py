import doctest
#A dictionary of grades and ranges
grade_dict = {"A": 80,"B": 70,"C": 60,"D": 50, "fail":0}

def grade(g_dict:dict,mark:int):
    """
    Checks the mark and prints the applicable grade by using the grade dictionary provided
    
    Examples:
    
    >>> grade({"A": 80,"B": 70,"C": 60,"D": 50, "fail":0}, 68)
    C
    done

    >>> grade({"A": 88,"B": 82,"C": 76,"D": 70, "fail":0}, 73)
    D
    done
    
    """
    for gr in g_dict:
        if mark >= g_dict[gr]:
            print(gr)
            break
    print("done")
    
doctest.testmod()