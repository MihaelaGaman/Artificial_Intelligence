def is_negative_literal(n):
    if n[0] == "neg":
        return True
    return False

def is_positive_literal(n):
    if n[0] != "neg":
        return True
    return False

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

# intoarce adevarat daca f este un termen
def is_term(f):
    return is_constant(f) or is_variable(f)

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


def get_recursive_pred(formula):
    p = get_premises(formula)

    for pi in p[0][1]:
        if not isinstance(pi[1], list):
                return pi[1]
        else:
            get_recursive_pred(pi[1][1])

