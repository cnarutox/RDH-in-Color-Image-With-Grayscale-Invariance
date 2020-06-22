function [stego, L_embedmess, L_a, tag, N] = addPEs(gray, cover, PER, PEB, pred_R, pred_B, sel_ind, lsb_ind, messL, D_T)
    R = double(cover(:, :, 1));
    G = double(cover(:, :, 2));
    B = double(cover(:, :, 3));
    cR = 0.299;
    cG = 0.587;
    cB = 0.114;
    [ht, wd] = size(G);
    mess = round(rand(1, messL));
    tags = zeros(1, wd * ht);
    ac_bit = 1;
    id = 0;
    tag = 0;
    L_embedmess = 1;

    for i = 2:ht - 1

        if L_embedmess >= messL
            break;
        end

        for j = 2:wd - 1

            id = id + 1;

            if id > length(sel_ind)
                break;
            end

            c_id = sel_ind(id);
            ii = floor((c_id - 1) / (ht - 2)) + 2;
            jj = mod((c_id - 1), (ht - 2)) + 2;

            %                  R0=R(ii,jj);B0=B(ii,jj);G0=G(ii,jj);
            %                  if round(cR*R0+cB*B0+cG*G(ii,jj))~=gray(ii,jj)
            %                     round(cR*R0+cB*B0+cG*G(ii,jj))-gray(ii,jj)
            %                  end
            PER(c_id) = 2 * PER(c_id) + mess(L_embedmess);
            PEB(c_id) = 2 * PEB(c_id) + ac_bit;
            M_R = PER(c_id) + pred_R(c_id);
            M_B = PEB(c_id) + pred_B(c_id);
            M_G = round((gray(ii, jj) - cR * M_R - cB * M_B) / cG);
            rec_G = round((gray(ii, jj) - cR * R(ii, jj) - cB * B(ii, jj)) / cG);
            ac_bit = abs(round(rec_G - G(ii, jj)));
            D = (R(ii, jj) - M_R)^2 + (G(ii, jj) - M_G)^2 + (B(ii, jj) - M_B)^2;
            %%%******测试
            %                     if ac_bit>1
            %                         ac_bit
            %                     end
            %%%******根据ac_bit恢复通道G
            %                     if ac_bit==1
            %                          if round(cR*R0+cB*B0+cG*(rec_G+1))==gray(ii,jj)
            %                              rec_G=rec_G+1;
            %                          else
            %                              rec_G=rec_G-1;
            %                          end
            %                     else
            %                         rec_G=G(ii,jj);
            %                     end
            %
            %                     if rec_G~=G(ii,jj)
            %                        rec_G-G(ii,jj)
            %                     end

            if (max([M_R M_G M_B]) > 255 || min([M_R M_G M_B]) < 0 || D > D_T)
                tags(id) = 1;
                %                          R(ii,jj)=R0;B(ii,jj)=B0;G(ii,jj)=G0;
            else
                tags(id) = 0;
                R(ii, jj) = M_R; G(ii, jj) = M_G; B(ii, jj) = M_B;
                L_embedmess = L_embedmess + 1;
            end

            if L_embedmess >= messL
                tag = 1;
                break;
            end

        end

    end

    N = id;
    tags = tags(1:id);

    if length(unique(tags)) > 1
        L_a = compresscoder(tags);
    else
        L_a = 1;
    end

    count = 0;
    L_a = L_a + 50;

    for id = 1:length(lsb_ind)

        if id > length(lsb_ind)
            break;
        end

        c_id = sel_ind(id);

        ii = floor((c_id - 1) / (ht - 2)) + 2;
        jj = mod((c_id - 1), (ht - 2)) + 2;

        if round(cR * R(ii, jj) + cG * G(ii, jj) + cB * 2 * floor(B(ii, jj) / 2)) == round(cR * R(ii, jj) + cG * G(ii, jj) + cB * (2 * floor(B(ii, jj) / 2) + 1))
            B(ii, jj) = 2 * floor(B(ii, jj) / 2) + round(rand());
            count = count + 1;

            if count > L_a
                break
            end

        end

    end

    if (count < L_a)
        tag = 0;
    end

    stego(:, :, 1) = R;
    stego(:, :, 2) = G;
    stego(:, :, 3) = B;
end
