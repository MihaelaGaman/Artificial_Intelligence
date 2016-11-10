from copy import deepcopy

def is_negative_literal(n):
    if n[0] == "neg":
        return True
    return False

def is_positive_literal(n):
    if n[0] != "neg":
        return True
    return False


def get_premises(formula):
    # TODO
    #return []
    return [get_args(n)[0] for n in get_args(formula) if is_negative_literal(n)]
    
def get_conclusion(formula):
    # TODO
    #pass
    return list(filter(is_positive_literal, get_args(formula)))[0]

def is_fact(formula):
    # TODO
    #pass
    return is_positive_literal(formula)

def is_rule(formula):
    # TODO
    #pass
    if get_head(formula) != get_head(make_or(make_atom("P"), make_atom("P"))):
        return False
    if not is_positive_literal(get_conclusion(formula)):
        return False
    return all(list(map(is_positive_literal, get_premises(formula))))

def has_args(f):
    return is_function_call(f) or is_sentence(f)


def get_premises(formula):
    return [get_args(n)[0] for n in get_args(formula) if is_negative_literal(n)]
    
def get_conclusion(formula):
    return list(filter(is_positive_literal, get_args(formula)))[0]

# pentru constante (de verificat), se intoarce valoarea constantei. Altfel, None
def get_value(f):
    if f[0] == "cnt":
        return f[1]
    return None

# pentru variabile (de verificat), se intoarce numele variabilei. Altfel, None
def get_name(f):
    if f[0] == "var":
        return f[1]
    return None

# pentru apeluri de functii, se intoarce numele functiei; pentru atomi, se intoarce numele predicatului; 
# pentru propozitii compuse, se intoarce un sir de caractere care reprezinta conectorul logic (~, A sau V)
# altfel, None
def get_head(f):
    if f[0] == "fct" or f[0] == "pred":
        return f[1]
    elif f[0] == "neg" or f[0] == "and" or f[0] == "or":
        return f[0]
    return None

# pentru propozitii sau apeluri de functii, se intoarce lista de argumente. Altfel, None
def get_args(f):
    if f[0] == "fct" or f[0] == "pred":
        return f[2]
    elif f[0] == "neg" or f[0] == "and" or f[0] == "or":
        return f[1]
    return None

# intoarce adevarat daca f este un termen constant
def is_constant(f):
    return f[0] == "cnt"

# intoarce adevarat daca f este un termen ce este o variabila
def is_variable(f):
    return f[0] == "var"

# intoarce adevarat daca f este un atom (aplicare a unui predicat)
def is_atom(f):
    return f[0] == "pred"

# intoarce adevarat daca f este o propozitie valida
def is_sentence(f):
    if f[0] == "pred" or f[0] == "neg" or f[0] == "and" or f[0] == "or":
        return True
    
    return False

# intoarce adevarat daca f este un apel de functie
def is_function_call(f):
    return f[0] == "fct"

# intoarce adevarat daca f este un termen
def is_term(f):
    return is_constant(f) or is_variable(f) or is_function_call(f)

# intoarce un termen constant, cu valoarea specificata
def make_const(value):
    return ("cnt", value)

# intoarce un termen care este o variabila, cu numele specificat
def make_var(name):
    return ("var", name)

# intoarce o formula formata dintr-un atom care este aplicarea 
# predicatului dat pe restul argumentelor date
def make_atom(predicate, *args):
    return ("pred", predicate, list(args))

# intoarce o formula care este negarea propozitiei date
def make_neg(sentence):
    return ("neg", [sentence])

# intoarce un termen care este un apel al functiei cu numele specificat, pe restul argumentelor date.
# E.g. pentru a construi termenul add[1, 2, 3] vom apela make_function_call(add, 1, 2, 3)
def make_function_call(name, *args):
    return ("fct", str(name), list(args))

# intoarce o formula care este conjunctia propozitiilor date
def make_and(sentence1, sentence2, *others):
    if others is not None:
        return ("and", [sentence1, sentence2] + list(others))
    else:
        return ("and", [sentence1, sentence2])

# intoarce o formula care este disjunctia propozitiilor date
def make_or(sentence1, sentence2, *others):
    if others is not None:
        return ("or", [sentence1, sentence2] + list(others))
    else:
        return ("or", [sentence1, sentence2])

def check_term(T):
    return (is_constant(T) and get_value(T) is not None) or \
    (is_variable(T) and get_name(T) is not None) or \
    (is_function_call(T) and callable(get_head(T)) and not [t for t in get_args(T) if not check_term(t)])

def check_atom(A):
    return is_atom(A) and get_head(A) is not None and not [t for t in get_args(A) if not check_term(t)]
dummy = make_atom("P")
and_name = get_head(make_and(dummy, dummy))
or_name = get_head(make_and(dummy, dummy))
neg_name = get_head(make_neg(dummy))

def check_sentence(S):
    return is_sentence(S) and (
        check_atom(S) or
        ((get_head(S) == and_name or get_head(S) == or_name) and len(get_args(S)) >= 2 and
             not [s for s in get_args(S) if not check_sentence(s)])
        or
        (get_head(S) == neg_name and len(get_args(S)) == 1 and check_sentence(get_args(S)[0]))
        )

def make_statement(conclusion, hypotheses):
    L = list(hypotheses)
    if not L:
        return conclusion
    L = [make_neg(s) for s in L]
    print L
    L.append(conclusion)
    return make_or(*L)

def add_statement(kb, conclusion, *hypotheses):
    s = make_statement(conclusion, hypotheses)
    if check_sentence(s) is not None:
        kb.append(s)
        #print("Added statement " + print_formula(s, True))
        return True
    print("Sentence does not check out ", result)
    return False

from functools import reduce

# intoarce formula sau apelul de functie date, in care argumentele au fost inlocuite cu lista new_args
# e.g. pentru formula p(x, y), inlocuirea argumentelor cu lista [1, 2] va rezulta in formula p(1, 2)
# Noua lista de argumente trebuie sa aiba aceeasi lungime cu numarul de argumente initial din formula
def replace_args(formula, new_args):
    if formula[0] == "fct" or formula[0] == "pred":
        if len(formula[2]) == len(new_args):
            return (formula[0], formula[1], new_args)
    elif formula[0] == "neg" or formula[0] == "and" or formula[0] == "or":
        if len(formula[1]) == len(new_args):
            return (formula[0], new_args)
    return None

# Aplica in formula f toate elementele din substitutia data si intoarce formula rezultata
def substitute(f, substitution):
    if substitution is None:
        return None
    if is_variable(f) and (get_name(f) in substitution):
        return substitute(substitution[get_name(f)], substitution)
    if has_args(f):
        return replace_args(f, [substitute(arg, substitution) for arg in get_args(f)])
    return f

from functools import reduce

# Verifica daca variabila v poate fi inlocuita cu termenul t, avand in vedere substitutia subst.
# Intoarce True daca v poate fi inlocuita cu t, si False altfel.
# Verificarea esueaza daca, avand in vedere si substitutia, variabila v apare in 
#  termenul t (deci inlocuirea lui v ar fi un proces infinit).
def occur_check(v, t, subst, topLevel = True):
    if is_constant(t):
        return True
    elif is_variable(t):
        if get_name(t) in subst:
            return occur_check(v, substitute(t, subst), subst, False)
        else:
            if topLevel:
                return True
            else:
                if get_name(v) != get_name(t):
                    return True
                else:
                    return False
    elif is_function_call(t):
        for arg in get_args(t):
            if occur_check(v, arg, subst, False) == False:
                return False
        return True
    
    return True

# Unifica formulele f1 si f2. Rezultatul unificarii este o substitutie (dictionar nume-variabila -> termen),
#  astfel incat daca se aplica substitutia celor doua formule, rezultatul este identic.
def unify(f1, f2, subst = None):
    # TODO
    #return {}
    stack = []
    if subst is None:
        subst = {}
    
    stack.append((f1, f2))
    
    while stack:
        (s, t) = stack.pop()
        while is_variable(s) and get_name(s) in subst:
            s = substitute(s, subst)
        while is_variable(t) and get_name(t) in subst:
            t = substitute(t, subst)
        if s != t:
            if is_variable(s):
                if not occur_check(s, t, subst):
                    return False
                subst[get_name(s)] = t
            elif is_variable(t):
                if not occur_check(t, s, subst):
                    return False
                subst[get_name(t)] = s
            elif has_args(s) and has_args(t):
                if get_head(s) != get_head(t) or len(get_args(s)) != len(get_args(t)):
                    return False
                for i in range(len(get_args(s))):
                    stack.append((get_args(s)[i], get_args(t)[i]))
            else:
                return False
    return subst

# Afiseaza formula f. 
# Daca argumentul return_result este True, 
# rezultatul nu este afisat la consola, ci intors.
def print_formula(f, return_result = False):
    ret = ""
    if is_term(f):
        if is_constant(f):
            ret += str(get_value(f))
        elif is_variable(f):
            ret += "?" + get_name(f)
        elif is_function_call(f):
            ret += get_head(f) + "[" + "".join([print_formula(arg, True) + "," for arg in get_args(f)])[:-1] + "]"
        else:
            ret += "???"
    elif is_atom(f):
        ret += get_head(f) + "(" + "".join([print_formula(arg, True) + ", " for arg in get_args(f)])[:-2] + ")"
    elif is_sentence(f):
        # negation, conjunction or disjunction
        args = get_args(f)
        if len(args) == 1:
            ret += get_head(f) + print_formula(args[0], True)
        else:
            ret += "(" + get_head(f) + "".join([" " + print_formula(arg, True) for arg in get_args(f)]) + ")"
    else:
        ret += "???"
    if return_result:
        return ret
    print ret



def print_KB(KB):
    print("KB now:")
    for s in KB:
        print("\t\t\t" + print_formula(s, True))


# def get_recursive_pred(formula):
#     p = get_premises(formula)

#     for pi in p[0][1]:
#         if not isinstance(pi[1], list):
#                 return pi[1]
#         else:
#             get_recursive_pred(pi[1][1])

def equal_terms(args1, args2):
    if len(args1) != len(args2):
        # Predicatele au aritate diferita
        return False
    for i, arg in enumerate(args2):
        if is_constant(arg):
            if not is_constant(args1[i]) or get_value(args1[i]) != get_value(arg):
                return False
        if is_variable(arg):
            if not is_variable(args1[i]) or get_name(args1[i]) != get_name(arg):
                return False
        if is_function_call(arg):
            if not is_function(args1[i]) or get_head(args1[i]) != get_head(arg):
                return False
            if not equal_terms(get_args(args1[i]), get_args(arg)):
                return False
    return True

def is_equal_to(a1, a2):
    # Nu verifica functii
    if not is_atom(a1):
        # a1 nu este atom
        return False
    if get_head(a1) != get_head(a2):
        # Predicatele au nume diferite
        return False
    return equal_terms(get_args(a1), get_args(a2))


def forward_chaining(kb, theorem, verbose=True):
    # Salvam baza de date originala, lucram cu o copie
    local_kb = deepcopy(kb)
    # Doua variabile care descriu starea cautarii
    got_new_facts = True   # s-au gasit fapte noi la ultima cuautare
    is_proved = False      # a fost demostrata teorema
    # Verificam daca teorema este deja demonstata
    for fact in filter(is_fact, local_kb):
        if is_equal_to(fact, theorem):
            return True
        if unify(fact, theorem):
            if verbose:
                print "This already in KB: "
                print_formula(fact)
            is_proved = True
            break
    while (not is_proved) and got_new_facts:
        got_new_facts = False
        for rule in filter(is_rule, local_kb):
            # Pentru fiecare regula
            new_facts = apply_rule(rule, list(filter(is_fact, local_kb)))
            new_facts = list(filter(lambda fact: not any(list(filter(lambda orig: is_equal_to(fact, orig), local_kb))), new_facts))
            if new_facts:
                if verbose:
                    print "Applied rule: "
                    print_formula(rule)
                got_new_facts = True
                for fact in new_facts:
                    #if verbose:
                    #    print("New fact: ", end = "")
                    #    print_formula(fact)
                    if unify(fact, theorem) != False:
                        is_proved = True
                        add_statement(local_kb, fact)
                        if verbose:
                            print "Now in KB: "
                            print_formula(fact)
                        break
                    add_statement(local_kb, fact)
            if is_proved:
                break
    if verbose:
        if is_proved:
            print "The theorem is TRUE!"
        else:
            print "The theorem is FALSE!"
    return is_proved

def apply_rule_2(rule, facts):
    if is_fact(rule):
        return [rule]
    solutions = []
    premises = get_premises(rule)
    premise = premises.pop()
    rest = make_statement(get_conclusion(rule), premises)
    for fact in facts:
        s = unify(premise, fact)
        if s != False:
            solutions.extend(apply_rule_2(substitute(rest, s), facts))
    return solutions

def get_all_solutions(premises, facts, subst):
    if premises:
        all_solutions = []
        for f in facts:
            new_subst = unify(premises[0], f, deepcopy(subst))
            if new_subst != False:
                all_solutions.extend(get_all_solutions(premises[1:], facts, new_subst))
    else:
        all_solutions = [subst]
    return all_solutions
        
def apply_rule(rule, facts):
    # TODO
    #return []
    
    # varianta 1
    #return list(map(lambda s: substitute(deepcopy(get_conclusion(rule)), s), get_all_solutions(get_premises(rule), facts, {})))

    # varianta 2
    return apply_rule_2(rule, facts)
    