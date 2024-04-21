class SchedulerCSP:
    def __init__(self, courses, loc_info_dict, course_info_dict, time_slots):
        self.courses = courses
        self.loc_info_dict = loc_info_dict
        self.course_info_dict = course_info_dict
        self.time_slots = time_slots
        self.variables = courses
        self.domains = self.initialize_domains()
        self.adjacency = self.initialize_adjacency()

    def initialize_domains(self):
        domains = {}
        for course in self.courses:
            pref_profs, student_count, duration, prereqs = self.course_info_dict[course]
            valid_locations = [loc for loc, capacity in self.loc_info_dict.items() if capacity >= student_count]
            domains[course] = [(prof, loc, time) for prof in pref_profs for loc in valid_locations for time in self.time_slots]
        return domains

    def initialize_adjacency(self):
        adjacency = {}
        for course in self.courses:
            adjacency[course] = [other_course for other_course in self.courses if other_course != course]
        return adjacency

    def check_overlap(self, start_time1, duration1, start_time2, duration2):
        end_time1 = start_time1 + duration1
        end_time2 = start_time2 + duration2
        return not ((start_time1 < start_time2 and end_time1 <= start_time2) or (start_time2 < start_time1 and end_time2 <= start_time1))

    def check_same_prof_same_overlap(self, prof1, start_time1, duration1, prof2, start_time2, duration2):
        if prof1 == prof2:
            return self.check_overlap(start_time1, duration1, start_time2, duration2)
        return False

    def check_same_loc_same_overlap(self, loc1, start_time1, duration1, loc2, start_time2, duration2):
        if loc1 == loc2:
            return self.check_overlap(start_time1, duration1, start_time2, duration2)
        return False

    def constraint_consistent(self, var1, val1, var2, val2):
        prof1, loc1, start1 = val1
        prof2, loc2, start2 = val2
        _, _, duration1, _ = self.course_info_dict[var1]
        _, _, duration2, _ = self.course_info_dict[var2]

        check1 = not (self.check_same_prof_same_overlap(prof1, start1, duration1, prof2, start2, duration2) or 
                      self.check_same_loc_same_overlap(loc1, start1, duration1, loc2, start2, duration2))

        # Prerequisite condition check
        if var2 in self.course_info_dict[var1][3] and start2 >= start1:
            return False
        if var1 in self.course_info_dict[var2][3] and start1 >= start2:
            return False

        return check1
    
    def check_partial_assignment(self, assignment):
        if assignment is None:
            return False
        for var1 in assignment:
            for var2 in assignment:
                if var1 != var2 and not self.constraint_consistent(var1, assignment[var1], var2, assignment[var2]):
                    return False
        return True

    def is_goal(self, assignment):
        if assignment is None or not self.check_partial_assignment(assignment):
            return False
        return len(assignment) == len(self.variables)