# coding = utf-8


from credit import exam_getter, error_string

if __name__ == "__main__":
    rev_val = exam_getter.get_exam_list("14xfdeng", "Smallfly2nd", 2014, 2015, 3)
    if rev_val[0]:
        print(rev_val[1])
    else:
        print(error_string.err_srt(rev_val[1]))

