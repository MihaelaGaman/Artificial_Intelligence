from helpers import *

def get_recursive_pred(formula):
    p = get_premises(formula)

    for pi in p[0][1]:
        if not isinstance(pi[1], list):
                return pi[1]
        else:
            get_recursive_pred(pi[1][1])


def main():
    # baza de date din starea initiala
    abox_kb = []
    tbox_kb = []

    # TBox
    add_statement(tbox_kb, make_atom('Woman', make_var('w')),\
                            make_and(make_atom('Person', make_var('w')),\
                            make_atom('Female', make_var('w'))))
    add_statement(tbox_kb, make_atom('Man', make_var('m')),\
                            make_and(make_atom('Person', make_var('m')),\
                            make_neg(make_atom('Woman', make_var('m')))))

    add_statement(tbox_kb, make_atom('Mother', make_var('x')),\
                            make_and(make_atom('Woman', make_var('x')),\
                                make_and(make_atom("hasChild", make_var("x"), make_var("y")),\
                                make_atom("Person", make_var("y")))))
    
    
    add_statement(tbox_kb, make_atom('Father', make_var('f')),\
                            make_and(make_atom('Man', make_var('f')),\
                                make_and(make_atom("hasChild", make_var("f"), make_var("y")),\
                                make_atom("Person", make_var("y")))))

    add_statement(tbox_kb, make_atom('Parent', make_var('f')),\
                            make_or(make_atom('Father', make_var('f')),\
                                make_atom("Mother", make_var("y"))))

    add_statement(tbox_kb, make_atom('Grandmother', make_var('x')),\
                            make_and(make_atom('Mother', make_var('x')),\
                                make_and(make_atom("hasChild", make_var("x"), make_var("y")),\
                                make_atom("Parent", make_var("y")))))

    # To be added:
    # MotherWithManyChildren = Mother and moreThan(hasChildren, 3)
    # MotherWithoutDaughter = Mother and Any(hasChild(not Woman))
    # Wife = Woman and Exists(hasHusband(Man))




    # ABox
    abox_kb.append(make_atom('MotherWithoutDaughter', make_const("MARY")))
    abox_kb.append(make_atom('Father', make_const("PETER")))
    abox_kb.append(make_atom('hasChild', make_const("PETER"), make_const("HARRY")))
    abox_kb.append(make_atom('hasChild', make_const("MARY"), make_const("PETER")))
    abox_kb.append(make_atom('hasChild', make_const("MARY"), make_const("PAUL")))

    print_KB(abox_kb)
    print_KB(tbox_kb)

    concepts = []
    print "Defined symbols:"
    for f in tbox_kb:
        c = get_conclusion(f)[1]
        concepts.append(c)
        print c

    print "Base symbols: "
    # for f in tbox_kb:
    #   p = get_premises(f)
    #   for pi in p[0][1]:
    #       if pi[1] not in concepts:
    #           print pi[1]
    for formula in tbox_kb:
       print get_recursive_pred(formula)

main()