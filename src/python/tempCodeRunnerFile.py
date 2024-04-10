 # If we found a better solution, return it
    if best_bp:
        return best_bp, min_error
    # Otherwise, return the current solution
    else:
        return bp, error_total