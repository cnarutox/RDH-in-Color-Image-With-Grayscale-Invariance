function [result] = LSpredictor(x, y, ref_value)
    % xy=x-y;
    % d=abs(xy(1)-xy(2))+abs(xy(1)-xy(3))+abs(xy(2)-xy(3));
    % d=x-y;
    %     if ( abs(d(1)-d(2))+abs(d(1)-d(3))+abs(d(2)-d(3)) )>( abs(y(1)-y(2))+abs(y(1)-y(3))+abs(y(2)-y(3)) )
    %         pred_value=MED(y);
    %     else
    %     d=abs(ref_value-MED(x));
    n = length(x);
    nn = min(length(unique(x)), length(unique(y)));
    k = max(nn - 1, 0);
    X = (zeros(n, k + 1));
    X0 = (zeros(1, k + 1));

    for i = 1:n

        for j = 1:k + 1
            X(i, j) = x(i)^(j - 1);

            if i == 1
                X0(1, j) = ref_value^(j - 1);
            end

        end

    end

    A = (X' * X)^-1 * X' * y';
    %         d=round(10*sum(abs(X*A-y')));
    pred_value = round(X0 * A);
    result = pred_value;

    if pred_value > max([y(1) y(2)])
        result = max([y(1) y(2)]);
    end

    if pred_value < min([y(1) y(2)])
        result = min([y(1) y(2)]);
    end

    %      end

end
