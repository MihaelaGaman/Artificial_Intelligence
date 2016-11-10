from helpers import *


def get_recursive_pred(formula, l):
    laux = deepcopy(l)
    if is_rule(formula):
        p = get_premises(formula)
    else:
        p = get_args(formula)

    for pi in p:
        if pi[0] == 'pred':
            laux.append(pi)
        elif pi[0] != 'fct':
            laux = get_recursive_pred(pi, laux)

    return laux


def prove_concept(concept, abox_kb, tbox_kb):
    pass


def included_in(c, concepts):
    for c1 in concepts:
        if c1[1] == c[1]:
            return True

    return False

def get_defined_concepts(tbox_kb):
    concepts = []
    print "Defined symbols:"

    for f in tbox_kb:
        c = get_conclusion(f)
        concepts.append(c)
        print c[1]

    return concepts

def get_base_concepts(tbox_kb):
    defined = get_defined_concepts(tbox_kb)
    base = []

    print "Base symbols: "
    for formula in tbox_kb:
        lc = get_recursive_pred(formula, [])
        for c in lc:
            if not included_in(c, defined) and not included_in(c, base):
                base.append(c)
                print c[1]

    return base

def get_true_premises(premise, l):
    laux = deepcopy(l)
    preds = get_args(premise)

    for p in preds:
        if p[0] == 'pred' and p[1] not in laux:
            laux.append(p[1])
        elif p[0] == 'and':
            laux = get_true_premises(p, laux)

    return laux


def prove_all(abox_kb, tbox_kb):
    local_abox = deepcopy(abox_kb)
    local_tbox = deepcopy(tbox_kb)

    defined = get_defined_concepts(tbox_kb)
    base = get_base_concepts(tbox_kb)

    to_be_proved = deepcopy(defined + base)

    constants = []

    # Get all the constants in ABOX
    for a in local_abox:
        for const in a[2]:
            c = make_const(const[1])
            if c not in constants:
                constants.append(c)

    print "Constants: ", constants


    # Get premises from theorem
    changed = True
    while changed:
        aux_abox = deepcopy(local_abox)
        changed = False

        for formula in local_tbox:
            hypo = get_conclusion(formula)
            premise = get_premises(formula)

            for a in aux_abox:
                if a[1] == hypo[1]:
                    arg = make_const(a[2][0][1])
                    for p in premise:
                        true_concepts = get_true_premises(p, [])
                        for name in true_concepts:
                            atom = make_atom(name, arg)
                            if atom not in local_abox:
                                changed = True
                                local_abox.append(atom)

            # Get true theorems
            for const in constants:
                for p in premise:
                    true_concepts = get_true_premises(p, [])
                    ok = True
                    for name in true_concepts:
                        atom = make_atom(name, const)
                        if atom not in local_abox:
                            ok = False
                    if ok == True:
                        ta = make_atom(hypo[1], const)
                        if ta not in local_abox:
                            changed = True
                            local_abox.append(ta)


    print_KB(local_abox)
    print_KB(abox_kb)

    #print forward_chaining(deepcopy(local_abox + local_tbox), make_atom("Mother", make_const("MARY")))

    # Get theorem from premises


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
                                make_and(make_function_call("hasChild", make_var("x"), make_var("y")),\
                                make_atom("Person", make_var("y")))))
    
    
    add_statement(tbox_kb, make_atom('Father', make_var('f')),\
                            make_and(make_atom('Man', make_var('f')),\
                                make_and(make_function_call("hasChild", make_var("f"), make_var("c")),\
                                make_atom("Person", make_var("c")))))

    add_statement(tbox_kb, make_atom('Parent', make_var('p')),\
                            make_or(make_atom('Father', make_var('p')),\
                                make_atom("Mother", make_var("p"))))

    add_statement(tbox_kb, make_atom('Grandmother', make_var('g')),\
                            make_and(make_atom('Mother', make_var('g')),\
                                make_and(make_function_call("hasChild", make_var("g"), make_var("z")),\
                                make_atom("Parent", make_var("z")))))

    add_statement(tbox_kb, make_atom('MotherWithManyChildren', make_var("mwmc")), \
                            make_and(make_atom('Mother', make_var('mwmc')), \
                                make_and(make_function_call('hasChild', make_var('mwmc'), make_var('c1')), \
                                    make_and(make_function_call('hasChild', make_var('mwmc'), make_var('c2')),\
                                        make_function_call('hasChild', make_var('mwmc'), make_var('c3'))))))

    add_statement(tbox_kb, make_atom('MotherWithoutDaughter', make_var('x')),\
                            make_and(make_atom('Woman', make_var('x')),\
                                make_neg(make_and(make_function_call("hasChild", make_var("x"), make_var("y")),\
                                make_atom("Woman", make_var("y"))))))

    add_statement(tbox_kb, make_atom('Wife', make_var('x')),\
                        make_and(make_atom('Woman', make_var('x')),\
                            make_and(make_function_call("hasHusband", make_var("x"), make_var("y")),\
                            make_atom("Man", make_var("y")))))

    KB = deepcopy(tbox_kb)


    # ABox
    abox_kb.append(make_atom('MotherWithoutDaughter', make_const("MARY")))
    abox_kb.append(make_atom('Father', make_const("PETER")))
    abox_kb.append(make_function_call('hasChild', make_const("PETER"), make_const("HARRY")))
    abox_kb.append(make_function_call('hasChild', make_const("MARY"), make_const("PETER")))
    abox_kb.append(make_function_call('hasChild', make_const("MARY"), make_const("PAUL")))

    for atom in abox_kb:
        KB.append(atom)

    # print_KB(abox_kb)
    # print_KB(tbox_kb)

    #print forward_chaining(deepcopy(KB), make_atom('Parent', make_const("PETER")))

    prove_all(abox_kb, tbox_kb)

main()